# tests/kafka/test_create_order_kafka.py
import pytest
import time
from tests.kafka.kafka_consumer import OrderKafkaConsumer
from tests.kafka.order_created_event import OrderCreatedEvent
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto


@pytest.fixture(scope="module")
def kafka_consumer():
    return OrderKafkaConsumer(topic="order-events")

def test_message_should_be_produced_to_kafka_after_successful_created_order(
    kafka_consumer, random_user, random_ingredient, faker_instance
):
    token = random_user.token
    order_client = OrderApiClient(token=token)
    body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())

    response = order_client.create_order(body)

    # Получаем сообщение из Kafka
    message = kafka_consumer.get_message(response.user.id, timeout_sec=10)
    print(message)
    assert message is not None, "Kafka message not found"

    event = OrderCreatedEvent(**message)

    assert response.id == event.orderId
    assert response.status == event.status
    assert [i.id for i in response.ingredients] == event.ingredientIds
    assert response.user.id == event.userId