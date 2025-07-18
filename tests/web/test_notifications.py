
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto
from tests.web.components.sidebar_component import SideBarComponent
from tests.web.pages.login_page import LoginPage


class TestUINotifications:

    def test_create_order_change_notification_count(self, driver, base_ui_url, random_user, random_ingredient, faker_instance):
        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("seller", "seller")
        orders_page = login_page.submit()
        orders_page.wait_for_page_loaded()

        sidebar = SideBarComponent(driver)
        count_before = sidebar.get_unread_notification_count()

        order_client = OrderApiClient(token=random_user().token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order_client.create_order(body)

        count_after = sidebar.get_unread_notification_count()

        assert count_before != count_after

    def test_change_status_order_notification_count(self, driver, base_ui_url, random_user, random_ingredient, faker_instance):
        customer_user = random_user(user_type="customer", create_new=False)

        order_client = OrderApiClient(token=customer_user.token)
        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_male())
        order_id = order_client.create_order(body).id

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("seller", "seller").submit().wait_for_page_loaded()

        sidebar = SideBarComponent(driver)
        pending_orders_page = sidebar.go_to_pending_orders_page()

        pending_orders_page.find_by_id(str(order_id)).change_status("DONE").update()

        sidebar.log_out()
        orders_page = login_page.fill_login_page("customer", "customer").submit().wait_for_page_loaded()
        status = orders_page.find_by_id(str(order_id)).get_status()
        assert status == "Выполнен"