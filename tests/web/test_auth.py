import pytest

from tests.web.pages.login_page import LoginPage
from tests.web.pages.orders_page import OrdersPage


@pytest.mark.usefixtures("driver", "base_ui_url")
class TestUIAuth:

    def test_success_login_redirects_to_orders(self, driver, base_ui_url):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        login_page.login_as("customer", "customer")

        orders_page = OrdersPage(driver)
        assert orders_page.is_visible(*orders_page.TITLE)


    def test_bad_credentials_shows_error(self, driver, base_ui_url):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.wait_loaded()
        error = login_page.login_with_error("fake", "data")
        assert "Неверный логин или пароль" in error