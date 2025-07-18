from typing import Any, Generator, List

import pytest
from tests.kafka.kafka_consumer import OrderKafkaConsumer
from tests.kafka.order_created_event import OrderCreatedEvent
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto


@pytest.fixture(scope="module")
def kafka_consumer() -> Generator[OrderKafkaConsumer, Any, None]:
    consumer = OrderKafkaConsumer(topic="order-events")
    yield consumer
    consumer.close()


def test_kafka_message_after_successful_order(
    kafka_consumer: OrderKafkaConsumer,
    random_user,
    random_ingredient: List[int],
    faker_instance,
) -> None:
    token = random_user().token
    response = OrderApiClient(token=token).create_order(
        CreateOrderDto(
            ingredientIds=random_ingredient,
            comment=faker_instance.name_male(),
        )
    )

    raw_event = kafka_consumer.get_message(user_id=response.user.id, timeout=10)
    print(raw_event)
    assert raw_event, "Kafka message not found"

    event = OrderCreatedEvent.from_dict(raw_event)

    assert event.orderId == response.id
    assert event.userId == response.user.id
    assert event.status == response.status
    assert event.ingredientIds == [i.id for i in response.ingredients]