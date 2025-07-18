from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..components.pending_order_component import PendingOrderComponent


class PendingOrdersPage(BasePage):
    TITLE = (By.XPATH, "//*[text()='Текущие заказы']")
    CARDS = (By.CSS_SELECTOR, "[data-testid^='pending-order-card-']")
    NO_ELEMENTS = (By.CSS_SELECTOR, "[data-testid='pending-orders-empty']")

    def get_orders(self):
        cards = self.driver.find_elements(*self.CARDS)
        return [PendingOrderComponent(card) for card in cards]

    def find_by_id(self, id_: str):
        selector = (By.CSS_SELECTOR, f"[data-testid='pending-order-card-{id_}']")
        cards = self.driver.find_elements(*selector)
        return PendingOrderComponent(cards[0]) if cards else None

    def find_by_comment(self, comment: str):
        for order in self.get_orders():
            if order.get_comment() == comment:
                return order
        return None

    def wait_for_page_loaded(self) -> 'PendingOrdersPage':
        self.driver.find_element(*self.TITLE)
        # Ждем, пока либо появится пустой блок, либо хотя бы одна карточка
        try:
            self.driver.find_element(*self.NO_ELEMENTS)
        except Exception:
            if not self.driver.find_elements(*self.CARDS):
                raise AssertionError('Нет ни одной карточки и нет пустого блока!')
        return self 