from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class OrderComponent:
    def __init__(self, root: WebElement):
        self.root = root

    @property
    def id(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "h6").text.replace("Заказ №", "").strip()

    @property
    def status(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "span.MuiChip-label").text

    @property
    def comment(self) -> str:
        return self.root.find_element(By.XPATH, ".//p[contains(text(),'Комментарий:')]").text.replace("Комментарий: ", "").strip()

    @property
    def date(self) -> str:
        return self.root.find_element(By.CSS_SELECTOR, "p[variant='body2']").text

    def delete(self) -> None:
        self.root.find_element(By.CSS_SELECTOR, "[data-testid^='orders-delete-btn-']").click()