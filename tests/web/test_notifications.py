import time

import pytest

from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto
from tests.web.components.sidebar_component import SideBarComponent
from tests.web.pages.login_page import LoginPage
from tests.web.pages.orders_page import OrdersPage


@pytest.mark.usefixtures("driver", "base_ui_url")
class TestUINotifications:

    def test_create_order_change_notification_count(self, driver, base_ui_url, random_user, random_ingredient, faker_instance):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        login_page.login_as("seller", "seller")

        sidebar = SideBarComponent(driver)
        count_before = sidebar.get_unread_notification_count()

        order_client = OrderApiClient(token=random_user(user_type="customer", create_new=False).token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order_client.create_order(body)

        time.sleep(1)
        count_after = sidebar.get_unread_notification_count()

        assert count_before != count_after

    def test_change_status_order_notification_count(self, driver, base_ui_url, random_user, random_ingredient, faker_instance):
        customer_user = random_user(user_type="customer", create_new=False)

        order_client = OrderApiClient(token=customer_user.token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order_id = order_client.create_order(body).id

        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        login_page.login_as("seller", "seller")

        sidebar = SideBarComponent(driver)
        pending_orders_page = sidebar.go_to_pending_orders_page().wait_loaded()

        component = pending_orders_page.order_by_id(str(order_id))
        component.set_status("DONE")
        component.update()

        sidebar.log_out()

        login_page.login_as("customer", "customer")
        orders_page = OrdersPage(driver)
        status = orders_page.order_by_id(str(order_id)).status
        assert status == "Выполнен"