from selenium.webdriver.common.by import By
from .base_page import BasePage


class RegisterPage(BasePage):
    USERNAME = (By.ID, "register-username")
    EMAIL    = (By.ID, "register-email")
    PASSWORD = (By.ID, "register-password")
    SUBMIT   = (By.ID, "register-submit")
    ERROR    = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]")

    def open(self, base_url: str):
        super().open(base_url)
        return self

    def fill_form(self, username: str, email: str, password: str):
        self.fill(*self.USERNAME, text=username)
        self.fill(*self.EMAIL, text=email)
        self.fill(*self.PASSWORD, text=password)
        return self

    def submit_success(self):
        self.click(*self.SUBMIT)

    def submit_error(self) -> str:
        self.click(*self.SUBMIT)
        return self.text(*self.ERROR)

    def wait_loaded(self):
        self.is_visible(*self.USERNAME)
        self.is_visible(*self.PASSWORD)
        return self