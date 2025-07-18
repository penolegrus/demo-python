
from tests.web.pages.login_page import LoginPage


class TestUIRegister:

    def test_should_register_new_user(self, driver, base_ui_url, faker_instance):
        login = faker_instance.user_name()
        password = faker_instance.password()
        email = faker_instance.email()

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        register_page = login_page.do_register()

        register_page.fill_register_page(login, password, email)
        register_page.success_submit()

        login_page.fill_login_page(login, password)
        orders_page = login_page.submit()

        orders_page.wait_for_page_loaded()

    def test_should_not_register_user_with_existing_username(self, driver, base_ui_url, faker_instance):
        username = "admin"
        password = faker_instance.password()
        email = faker_instance.email()

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        register_page = login_page.do_register()

        register_page.fill_register_page(username, password, email)
        register_page.error_submit()
        register_page.check_alert_message("Username already exists")

    def test_should_not_register_user_with_existing_email(self, driver, base_ui_url, faker_instance):
        username = faker_instance.user_name()
        password = faker_instance.password()
        email = "admin@admin.ru"

        driver.get(base_ui_url)
        login_page = LoginPage(driver)
        register_page = login_page.do_register()

        register_page.fill_register_page(username, password, email)
        register_page.error_submit()
        register_page.check_alert_message("Email already exists")
