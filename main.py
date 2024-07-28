import asyncio
import os
import random

import dotenv
from core.base_model import ProcessorProvider, Processor, ProcessorState
from core.base_processor import StatePropagationProviderRouterStateSyncStore, StatePropagationProviderDistributor, \
    StatePropagationProviderRouterStateRouter
from core.messaging.base_message_consumer_processor import BaseMessageConsumerProcessor
from core.messaging.base_message_router import Router
from core.messaging.nats_message_provider import NATSMessageProvider
from core.processor_state import State
from db.processor_state_db_storage import PostgresDatabaseStorage
from processor_question_answer import AnthropicQuestionAnswerProcessor

dotenv.load_dotenv()

# database related
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres1@localhost:5432/postgres")

# Message Routing File (
#   Used for routing processed messages, e.g: input comes in,
#   processed and output needs to be routed to the connected edges/processors
# )
ROUTING_FILE = os.environ.get("ROUTING_FILE", '.routing.yaml')
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


# state storage specifically to handle this processor state (stateless obj)
storage = PostgresDatabaseStorage(
    database_url=DATABASE_URL,
    incremental=True
)

message_provider = NATSMessageProvider()

# routing the persistence of individual state entries to the state sync store topic
router = Router(
    provider=message_provider,
    yaml_file=ROUTING_FILE
)

# find the monitor route for telemetry updates
monitor_route = router.find_route("processor/monitor")
state_router_route = router.find_route("processor/state/router")
state_sync_route = router.find_route('processor/state/sync')
anthropic_route_subscriber = router.find_route_by_subject("processor.models.anthropic")

state_propagation_provider = StatePropagationProviderDistributor(
    propagators=[
        StatePropagationProviderRouterStateSyncStore(route=state_sync_route),
        StatePropagationProviderRouterStateRouter(route=state_router_route)
    ]
)


class MessagingConsumerAnthropic(BaseMessageConsumerProcessor):
    # def create_processor(self, provider: ProcessorProvider, output_state: State):
    def create_processor(self,
                         processor: Processor,
                         provider: ProcessorProvider,
                         output_processor_state: ProcessorState,
                         output_state: State):

        processor = AnthropicQuestionAnswerProcessor(
            # storage class information
            state_machine_storage=storage,

            # state processing information
            output_state=output_state,
            provider=provider,
            processor=processor,
            output_processor_state=output_processor_state,

            # state information routing routers
            monitor_route=self.monitor_route,
            state_propagation_provider=state_propagation_provider
        )

        return processor

    # async def execute(self, consumer_message_mapping: dict):
    #     # submit completed execution
    #     await self.post_execute(
    #         consumer_message_mapping=consumer_message_mapping
    #     )


if __name__ == '__main__':
    consumer = MessagingConsumerAnthropic(
        storage=storage,
        route=anthropic_route_subscriber,
        monitor_route=monitor_route
    )

    # TODO think this through - important for workload creation. Here we randomly select a consumer number,
    #  and hope it does not collide with another consumer; if it does, then the consumer will throw an error
    #  and should exit, whereby next choosing a different number. Eventually, the consumer will find a spot.
    consumer_no = random.randint(0, 20)     # this should be a workload identity subscription

    consumer.setup_shutdown_signal()
    asyncio.get_event_loop().run_until_complete(consumer.start_consumer(consumer_no=consumer_no))
