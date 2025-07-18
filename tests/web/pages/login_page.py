from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "login-username")
    PASSWORD = (By.ID, "login-password")
    SUBMIT   = (By.ID, "login-submit")
    REGISTER = (By.CSS_SELECTOR, "a[href='/register']")
    ERROR    = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]")

    def open(self, base_url: str):
        super().open(base_url)
        return self

    def login_as(self, username: str, password: str):
        self.fill(*self.USERNAME, text=username)
        self.fill(*self.PASSWORD, text=password)
        self.click(*self.SUBMIT)

    def login_with_error(self, username: str, password: str) -> str:
        self.fill(*self.USERNAME, text=username)
        self.fill(*self.PASSWORD, text=password)
        self.click(*self.SUBMIT)
        return self.text(*self.ERROR)

    def go_to_register(self):
        self.click(*self.REGISTER)

    def wait_loaded(self):
        self.is_visible(*self.USERNAME)
        self.is_visible(*self.PASSWORD)
        return self