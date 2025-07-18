from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class PendingOrderComponent:
    def __init__(self, root: WebElement):
        self.root = root

    @property
    def id(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-id-']").text.replace("Заказ №", "").strip()

    @property
    def comment(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-comment-']").text.replace("Комментарий: ", "").strip()

    def set_status(self, new_status: str):
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-status-select-']").click()
        self.root.find_element(By.XPATH, f"//li[@data-value='{new_status}']").click()
        return self

    def update(self) -> None:
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-update-btn-']").click()

    def delete(self) -> None:
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-delete-btn-']").click()