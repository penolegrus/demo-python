from selenium.webdriver.common.by import By
from tests.web.pages.base_page import BasePage
from tests.web.components.pending_order_component import PendingOrderComponent
from typing import List, Optional


class PendingOrdersPage(BasePage):
    TITLE       = (By.XPATH, "//*[text()='Текущие заказы']")
    CARD        = (By.CSS_SELECTOR, "[data-testid^='pending-order-card-']")
    EMPTY_BLOCK = (By.CSS_SELECTOR, "[data-testid='pending-orders-empty']")

    def open(self, base_url: str) -> "PendingOrdersPage":
        super().open(base_url)
        return self.wait_loaded()

    def wait_loaded(self) -> "PendingOrdersPage":
        self.is_visible(*self.TITLE)
        # карточки или пустой блок — одно из двух
        if not (self.driver.find_elements(*self.CARD) or self.driver.find_elements(*self.EMPTY_BLOCK)):
            raise AssertionError("Нет ни карточек, ни пустого блока")
        return self

    @property
    def orders(self) -> List[PendingOrderComponent]:
        return [PendingOrderComponent(el) for el in self.driver.find_elements(*self.CARD)]

    def order_by_id(self, id_: str) -> Optional[PendingOrderComponent]:
        selector = (By.CSS_SELECTOR, f"[data-testid='pending-order-card-{id_}']")
        els = self.driver.find_elements(*selector)
        return PendingOrderComponent(els[0]) if els else None

    def order_by_comment(self, comment: str) -> Optional[PendingOrderComponent]:
        return next((o for o in self.orders if o.comment == comment), None)