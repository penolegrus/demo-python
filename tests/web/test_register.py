import pytest

from tests.web.pages.login_page import LoginPage
from tests.web.pages.orders_page import OrdersPage
from tests.web.pages.register_page import RegisterPage


@pytest.mark.usefixtures("driver", "base_ui_url")
class TestUIRegister:

    def test_register_new_user(self, driver, base_ui_url, faker_instance):
        login    = faker_instance.user_name()
        password = faker_instance.password()
        email    = faker_instance.email()

        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.go_to_register()

        register_page = RegisterPage(driver)
        register_page.fill_form(login, email, password)
        register_page.submit_success()

        login_page.login_as(login, password)
        orders_page = OrdersPage(driver)
        assert orders_page.is_visible(*orders_page.TITLE)

    def test_reject_existing_username(self, driver, base_ui_url, faker_instance):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.go_to_register()

        register_page = RegisterPage(driver)
        register_page.fill_form("admin", faker_instance.email(), faker_instance.password())
        error = register_page.submit_error()

        assert "Username already exists" in error

    def test_reject_existing_email(self, driver, base_ui_url, faker_instance):
        login_page = LoginPage(driver)
        login_page.open(base_ui_url)
        login_page.go_to_register()

        register_page = RegisterPage(driver)

        register_page.fill_form(faker_instance.user_name(), "admin@admin.ru", faker_instance.password())
        error = register_page.submit_error()

        assert "Email already exists" in error