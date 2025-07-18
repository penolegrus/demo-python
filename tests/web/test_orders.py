from tests.web.components.sidebar_component import SideBarComponent
from tests.web.pages.login_page import LoginPage


class TestUIOrders:

    def test_create_order(self, driver, base_ui_url, faker_instance):
        comment = faker_instance.password()

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("customer", "customer")
        orders_page = login_page.submit()
        orders_page.wait_for_page_loaded()

        orders_page.create_new_order(comment)
        order = orders_page.find_by_comment(comment)
        assert order is not None

    def test_check_order_appears_by_seller(self, driver, base_ui_url, faker_instance):
        comment = faker_instance.password()

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("customer", "customer")
        orders_page = login_page.submit()
        orders_page.wait_for_page_loaded()

        orders_page.create_new_order(comment)
        order_id = orders_page.find_by_comment(comment).get_id()

        SideBarComponent(driver).log_out()

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("seller", "seller")

        orders_page = login_page.submit()
        order = orders_page.find_by_id(order_id)
        assert order is not None

