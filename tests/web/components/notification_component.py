from selenium.webdriver.common.by import By

class NotificationComponent:
    def __init__(self, root):
        self.root = root

    def get_id(self) -> str:
        text = self.root.find_element(By.CSS_SELECTOR, "[data-testid^='notification-message-']").text
        if "№" in text:
            return text.split("№", 1)[1].strip()
        return None

    def get_message(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid^='notification-message-']").text

    def message_contains(self, text: str) -> bool:
        return text in self.get_message()

    def get_date(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid^='notification-date-']").text

    def get_type(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid^='notification-type-chip-']").text

    def type_text_is(self, expected_text: str) -> bool:
        return self.get_type() == expected_text

    def is_read(self) -> bool:
        return len(self.root.find_elements(By.CSS_SELECTOR, "[data-testid^='notification-read-chip-']")) > 0

    def mark_as_read(self):
        btns = self.root.find_elements(By.CSS_SELECTOR, "[data-testid^='notification-mark-read-btn-']")
        if btns:
            btns[0].click() 