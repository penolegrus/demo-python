import time

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