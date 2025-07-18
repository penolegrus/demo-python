from tests.rest.clients.order_client import OrderApiClient
from tests.rest.clients.notification_client import NotificationApiClient
from tests.rest.models.models import CreateOrderDto
import time

class TestOrder:
    def test_get_all_orders_returns_only_own_orders(self, random_user, random_ingredient, faker_instance):
        token = random_user().token
        order_client = OrderApiClient(token=token)

        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_female())
        order = order_client.create_order(body)
        orders = order_client.get_all_orders()
        assert orders
        found = next((o for o in orders if o.id == order.id), None)
        assert found is not None
        assert found.comment == body.comment

    def test_create_order_notify_seller(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        notification_client = NotificationApiClient(token=random_user(user_type="seller").token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order = order_client.create_order(body)
        # Polling for notification
        start = time.time()
        notification = None
        while time.time() - start < 5:
            notifications = notification_client.get_notifications()
            notification = next((n for n in notifications if n.orderId == order.id), None)
            if notification:
                break
            time.sleep(1)
        assert notification is not None

    def test_change_order_status_notify_customer(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        notification_client = NotificationApiClient(token=random_user(user_type="customer").token)

        seller_order_client = OrderApiClient(token=random_user(user_type="seller").token)

        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order = order_client.create_order(body)
        seller_order_client.update_order_status(order.id, "INPROGRESS")

        start = time.time()
        notification = None
        while time.time() - start < 5:
            notifications = notification_client.get_notifications()
            notification = next((n for n in notifications if n.orderId == order.id), None)
            if notification:
                break
            time.sleep(1)

        assert notification is not None
        assert "INPROGRESS" in notification.message
        assert notification.status == "UNREAD"

    def test_change_order_status_done_seller_not_see_pending(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        seller_order_client = OrderApiClient(token=random_user(user_type="seller").token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order = order_client.create_order(body)
        seller_order_client.update_order_status(order.id, "DONE")
        pending_orders = seller_order_client.get_pending_orders()
        assert all(o.id != order.id for o in pending_orders)

    def test_get_order_by_id(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        created = order_client.create_order(body)
        fetched = order_client.get_order_by_id(created.id)
        assert fetched.id == created.id

    def test_delete_order_by_id(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_female())
        created = order_client.create_order(body)
        resp = order_client.delete_order_by_id(created.id)
        assert resp.status_code == 204

    def test_get_pending_orders_seller(self, random_user, random_ingredient, faker_instance):
        order_client = OrderApiClient(token=random_user(user_type="customer").token)
        seller_order_client = OrderApiClient(token=random_user(user_type="seller").token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_female())
        order = order_client.create_order(body)
        pending = seller_order_client.get_pending_orders()
        assert any(o.id == order.id for o in pending) 