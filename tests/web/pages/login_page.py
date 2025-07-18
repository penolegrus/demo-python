from selenium.webdriver.common.by import By

from tests.web.pages.orders_page import OrdersPage
from .base_page import BasePage
from .register_page import RegisterPage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "login-username")
    PASSWORD_INPUT = (By.ID, "login-password")
    SUBMIT_BUTTON = (By.ID, "login-submit")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "a[href='/register']")
    ERROR_CONTAINER = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]")

    def do_register(self) -> RegisterPage:
        self.wait_for_element(*self.REGISTER_BUTTON).click()
        return RegisterPage(self.driver)

    def fill_login_page(self, username: str, password: str) -> 'LoginPage':
        self.set_username(username)
        self.set_password(password)
        return self

    def submit(self) -> 'OrdersPage':
        self.wait_for_element(*self.SUBMIT_BUTTON).click()
        return OrdersPage(self.driver)

    def set_username(self, username: str) -> 'LoginPage':
        self.wait_for_element(*self.USERNAME_INPUT).clear()
        self.wait_for_element(*self.USERNAME_INPUT).send_keys(username)
        return self

    def set_password(self, password: str) -> 'LoginPage':
        self.wait_for_element(*self.PASSWORD_INPUT).clear()
        self.wait_for_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def check_error(self, error: str) -> 'LoginPage':
        elem = self.wait_for_element(*self.ERROR_CONTAINER)
        assert error in elem.text
        return self

    def wait_for_page_loaded(self) -> 'LoginPage':
        self.wait_for_element(*self.USERNAME_INPUT)
        self.wait_for_element(*self.PASSWORD_INPUT)
        return self 