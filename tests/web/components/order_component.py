from selenium.webdriver.common.by import By

class OrderComponent:
    def __init__(self, root):
        self.root = root

    def get_id(self) -> str:
        text = self.root.find_element(By.TAG_NAME, "h6").text
        return text.replace("Заказ №", "").strip()

    def get_status(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "span.MuiChip-label").text

    def get_comment(self) -> str:
        elems = self.root.find_elements(By.XPATH, ".//p[contains(text(),'Комментарий:')]")
        if elems:
            return elems[0].text.replace("Комментарий: ", "").strip()
        return ""

    def get_date(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "p[variant='body2']").text

    def delete(self):
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='orders-delete-btn-']").click() 