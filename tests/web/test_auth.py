from tests.web.pages.login_page import LoginPage
from tests.web.pages.orders_page import OrdersPage


class TestUIAuth:

    def test_main_page_should_be_displayed_after_success_login(self, driver, base_ui_url):
        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        login_page.fill_login_page("customer", "customer")
        login_page.submit()

        orders_page = OrdersPage(driver)
        orders_page.wait_for_page_loaded()

    def test_user_should_stay_on_login_page_after_login_with_bad_credentials(self, driver, base_ui_url):
        driver.get(base_ui_url)
        login_page = LoginPage(driver)

        login_page.fill_login_page("fake", "data")
        login_page.submit()
        login_page.check_error("Неверный логин или пароль")