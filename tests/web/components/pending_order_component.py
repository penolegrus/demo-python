from selenium.webdriver.common.by import By

class PendingOrderComponent:
    def __init__(self, root):
        self.root = root

    def get_id(self) -> str:
        text = self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-id-']").text
        return text.replace("Заказ №", "").strip()

    def get_comment(self) -> str:
        elems = self.root.find_elements(By.CSS_SELECTOR, "[data-testid^='pending-order-comment-']")
        if elems:
            return elems[0].text.replace("Комментарий: ", "").strip()
        return ""

    def change_status(self, new_status: str):
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-status-select-']").click()
        xpath = f"//li[@data-value='{new_status}']"
        self.root.find_element(By.XPATH, xpath).click()
        return self

    def update(self):
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-update-btn-']").click()

    def delete(self):
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='pending-order-delete-btn-']").click() 