from selenium.webdriver.common.by import By
from .base_page import BasePage
from .login_page import LoginPage

class RegisterPage(BasePage):
    USERNAME_INPUT = (By.ID, "register-username")
    EMAIL_INPUT = (By.ID, "register-email")
    PASSWORD_INPUT = (By.ID, "register-password")
    SUBMIT_BUTTON = (By.ID, "register-submit")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href='/register']")
    ERROR_CONTAINER = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]")

    def fill_register_page(self, username: str, password: str, email: str) -> 'RegisterPage':
        self.set_username(username)
        self.set_email(email)
        self.set_password(password)
        return self

    def set_username(self, username: str) -> 'RegisterPage':
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        return self

    def set_email(self, email: str) -> 'RegisterPage':
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        return self

    def set_password(self, password: str) -> 'RegisterPage':
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        return self

    def success_submit(self) -> LoginPage:
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
        return LoginPage(self.driver)

    def error_submit(self) -> 'RegisterPage':
        self.driver.find_element(*self.SUBMIT_BUTTON).click()
        return self

    def wait_for_page_loaded(self) -> 'RegisterPage':
        self.driver.find_element(*self.USERNAME_INPUT)
        self.driver.find_element(*self.PASSWORD_INPUT)
        return self

    def check_alert_message(self, error_message: str) -> 'RegisterPage':
        elem = self.driver.find_element(*self.ERROR_CONTAINER)
        assert error_message in elem.text
        return self 