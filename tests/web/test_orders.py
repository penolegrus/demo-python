import pytest

from tests.web.components.sidebar_component import SideBarComponent
from tests.web.pages.login_page import LoginPage
from tests.web.pages.orders_page import OrdersPage
from tests.web.pages.pending_orders_page import PendingOrdersPage


@pytest.mark.usefixtures("driver", "base_ui_url")
class TestUIOrders:

    def test_create_order(self, driver, base_ui_url, faker_instance):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        login_page.login_as("customer", "customer")

        orders_page = OrdersPage(driver)

        comment = faker_instance.password()
        orders_page.create_order(comment)
        assert orders_page.order_by_comment(comment) is not None

    def test_order_visible_to_seller(self, driver, base_ui_url, faker_instance):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        login_page.login_as("customer", "customer")

        orders_page = OrdersPage(driver)

        comment = faker_instance.password()
        orders_page.create_order(comment)

        order_id = orders_page.order_by_comment(comment).id

        # выходим и заходим как продавец
        side_bar = SideBarComponent(driver)
        side_bar.log_out()

        login_page.wait_loaded()
        login_page.login_as("seller", "seller")

        side_bar.go_to_pending_orders_page()
        pending_order_page = PendingOrdersPage(driver)
        order = pending_order_page.order_by_id(order_id)

        assert order is not None