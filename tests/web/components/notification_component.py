from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class NotificationComponent:
    def __init__(self, root: WebElement):
        self.root = root

    @property
    def message(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid='notification-message']").text

    @property
    def type(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid='notification-type-chip']").text

    @property
    def is_read(self) -> bool:
        return bool(self.root.find_elements(By.CSS_SELECTOR, "[data-testid='notification-read-chip']"))

    def mark_as_read(self) -> None:
        btn = self.root.find_elements(By.CSS_SELECTOR, "[data-testid='notification-mark-read-btn']")
        if btn:
            btn[0].click()