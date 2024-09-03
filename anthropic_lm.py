import json
import os
import uuid
from typing import List

import dotenv
import nats.aio.msg
from core.base_model import ProcessorStatusCode

from core.base_processor_lm import BaseProcessorLM
from core.messaging.base_message_route_model import BaseRoute
from core.monitored_processor_state import MonitoredUsage

from logger import log
from anthropic import HUMAN_PROMPT, AI_PROMPT, Anthropic
from core.utils.general_utils import parse_response_strip_assistant_message

from pydantic import BaseModel, Field
from typing import Any

dotenv.load_dotenv()

logging = log.getLogger(__name__)
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)
logging.info(f'**** ANTHROPIC API KEY (last 4 chars): {anthropic_api_key[-4:]} ****')


class ProcessRequest(BaseModel):
    id: str
    process_id: str = Field(alias="processId")
    operation: str
    payload: List[dict]

    class Config:
        populate_by_name = True
        alias_generator = None
        allow_population_by_field_name = True

    def model_dump(self, **kwargs):
        kwargs['by_alias'] = True
        return super().model_dump(**kwargs)

    def dict(self, **kwargs):
        kwargs['by_alias'] = True
        return super().dict(**kwargs)


class ProcessReply(BaseModel):
    id: str
    payload: List[dict]  # Equivalent to json.RawMessage in Go, assuming it's binary JSON

    request_id: str = Field(alias="requestId")
    request_process_id: str = Field(alias="processId")


class AnthropicQuestionAnswerProcessor(BaseProcessorLM, MonitoredUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MonitoredUsage.__init__(self, **kwargs)

        self.anthropic = Anthropic(
            # This is the default and can be omitted
            api_key=anthropic_api_key,
        )

    async def query_data_source(self, input_data: Any, instruction: str):
        ds = "3be41212-16e9-4ccd-96fb-08f54d69f49c"
        datasource_subject = f"datasource.{ds}"

        ds_route = self.stream_route.clone(route_config_updates={
            "subject": datasource_subject,
            "name": datasource_subject.replace("-", "_")
        })
        request_id = str(uuid.uuid4())[-12:]
        if not isinstance(ds_route, BaseRoute):
            logging.warning(f"datasource must be of type base route or subclass, unsupported type {ds_route}")
            return

        # def cb(msg: Any):
        #     print(f"**************** {msg} *************\n")

        try:
            await ds_route.subscribe()
            process_request = ProcessRequest(
                id=request_id,
                process_id=self.processor.id,
                operation="query",
                payload=[{
                    "query_state": [input_data],
                    "instruction": instruction
                }]
            ).model_dump()
            # await ds_route.

            reply = await ds_route.request(process_request)
        except Exception as e:
            logging.error(e)

        # await ds_route.disconnect()

        logging.info("*******************")

        # if the reply is not of msg type then it must have failed
        if not isinstance(reply, nats.aio.msg.Msg):
            # TODO log a warning to the monitor
            warning = f"failed to received response for request: {request_id}, datasource: {datasource_subject}"
            await self.send_processor_state_update(
                self.output_processor_state.id,
                status=ProcessorStatusCode.RUNNING,
                data=f'failed to process data through request: {request_id}, datasource: {datasource_subject}')

            logging.warning(warning)

        try:
            json_data = json.loads(reply.data)
            process_reply = ProcessReply(**json_data)
            return process_reply
        except:
            return None

    async def _stream(self, input_data: Any, template: str):
        if not template:
            template = str(input_data)

        # rendered message we want to submit to the model
        message_list = self.derive_messages_with_session_data_if_any(template=template, input_data=input_data)

        # system messages from datasource given the template prompt
        # query_reply = await self.query_data_source(input_data=input_data, instruction=template)

        # add both the user and assistant generated data to the session
        system_message = ""
        # if query_reply and query_reply.payload:
        #     yield f"ds reply id: {query_reply.id}\n"
        #     system_message = json.dumps(query_reply.payload)

        # Start a streaming completion
        with self.anthropic.messages.stream(
                model=self.provider.version,
                max_tokens=1024,
                system=system_message,
                messages=message_list
        ) as stream:
            # Iterate over the streamed responses and yield the content
            output_data = []
            for content in stream.text_stream:
                output_data.append(content)
                yield content

            # After the stream is complete, get the final response object
            final_response = stream.get_final_message()

            # send input and output token counts
            await self.send_usage_input_tokens(final_response.usage.input_tokens)
            await self.send_usage_output_tokens(final_response.usage.output_tokens)

            # if system_message:
            #     yield f"{system_message}"
            #
            # add both the user and assistant generated data to the session

            self.update_session_data(
                input_data=input_data,
                input_template=template,
                output_data="".join(output_data))

            # logging.debug(f"\n\nRoute {self.processor.id}:", stream.get_final_message().usage)

    async def _execute(self, user_prompt: str, system_prompt: str, values: dict):
        message = self.anthropic.messages.create(
            model=self.provider.version,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        raw_response = message.content[0].text

        # send input and output token counts
        await self.send_usage_input_tokens(message.usage.input_tokens)
        await self.send_usage_output_tokens(message.usage.output_tokens)

        # raw_response = completion.completion
        return parse_response_strip_assistant_message(raw_response=raw_response)
