import json
import os
import dotenv

from core.base_processor_lm import BaseProcessorLM
from logger import log
from anthropic import HUMAN_PROMPT, AI_PROMPT, Anthropic
from core.utils.general_utils import parse_response_strip_assistant_message
from tenacity import retry, wait_exponential, wait_random, retry_if_not_exception_type

dotenv.load_dotenv()

logging = log.getLogger(__name__)
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)
logging.info(f'**** ANTHROPIC API KEY (last 4 chars): {anthropic_api_key[-4:]} ****')


class AnthropicQuestionAnswerProcessor(BaseProcessorLM):

    def __init__(self,  *args, **kwargs):
        super().__init__(**kwargs)

        self.anthropic = Anthropic(
            # This is the default and can be omitted
            api_key=anthropic_api_key,
        )

    def _execute(self, user_prompt: str, system_prompt: str, values: dict):
        message = self.anthropic.messages.create(
            model=self.provider.version,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        raw_response = message.content[0].text

        # raw_response = completion.completion
        return parse_response_strip_assistant_message(raw_response=raw_response)

