import time

import pytest

from tests.conftest import poll_until
from tests.rest.clients.notification_client import NotificationApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto


def wait_for_notification(order_id, notification_client, timeout=5, poll_interval=2):
    start = time.time()
    while time.time() - start < timeout:
        notifications = notification_client.get_notifications()
        for n in notifications:
            if n.orderId == order_id:
                return n
        time.sleep(poll_interval)
    return None


class TestNotifications:

    def test_create_order_notify_seller(self, random_user, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        notification_client = NotificationApiClient(token=random_user(user_type="seller").token)

        body = CreateOrderDto(ingredientIds=[1, 2], comment=faker_instance.ascii_free_email())
        order = order_client.create_order(body)
        notification = wait_for_notification(order.id, notification_client)
        assert notification is not None

        notification_client.read_notification(notification.id)
        notifications = notification_client.get_notifications()

        updated = next((n for n in notifications if n.id == notification.id), None)
        assert updated is not None
        assert updated.status == "READ"

    def test_read_all_notifications(self, random_user, faker_instance):
        notification_client = NotificationApiClient(token=random_user(user_type="seller").token)
        order_client = OrderApiClient(token=random_user(user_type="customer").token)

        notification_client.delete_all_notifications()

        body = CreateOrderDto(ingredientIds=[1], comment=faker_instance.ascii_free_email())
        order_client.create_order(body)
        order_client.create_order(body)
        order_client.create_order(body)

        # Ждем, пока появится 3 уведомления
        start = time.time()
        while True:
            notifications = notification_client.get_notifications()
            if len(notifications) == 3 or time.time() - start > 5:
                break
            time.sleep(1)

        notification_client.read_all_notifications()
        notifications_after = notification_client.get_notifications()
        assert all(x.status == "READ" for x in notifications_after)

    def test_delete_all_notifications(self, random_user, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        notification_client = NotificationApiClient(token=random_user(user_type="seller").token)

        body = CreateOrderDto(ingredientIds=[1], comment=faker_instance.ascii_free_email())
        body2 = CreateOrderDto(ingredientIds=[2], comment=faker_instance.ascii_free_email())
        order_client.create_order(body)
        order_client.create_order(body2)

        notification_client.delete_all_notifications()
        notifications = notification_client.get_notifications()

        assert notifications == []

@pytest.mark.usefixtures("customer_client", "notification_client")
class TestNotificationsV2:
    def test_seller_reads_single(self, customer_client, notification_client, faker):
        order = customer_client.create_order(CreateOrderDto(ingredientIds=[1], comment=faker.word()))
        notif = poll_until(lambda: next((n for n in notification_client.get_notifications() if n.orderId == order.id), None))
        notification_client.read_notification(notif.id)
        assert next(n for n in notification_client.get_notifications() if n.id == notif.id).status == "READ"

    def test_bulk_read_and_delete(self, customer_client, notification_client, faker):
        # создаём 3 заказа → 3 уведомления
        for _ in range(3):
            customer_client.create_order(CreateOrderDto(ingredientIds=[1], comment=faker.word()))

        notifications = poll_until(lambda: notification_client.get_notifications() if len(notification_client.get_notifications()) == 3 else None)
        assert notifications
        notification_client.read_all_notifications()
        assert all(n.status == "READ" for n in notification_client.get_notifications())
        notification_client.delete_all_notifications()
        assert notification_client.get_notifications() == []