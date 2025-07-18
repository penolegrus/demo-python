from selenium.webdriver.common.by import By
from .base_page import BasePage
import random

from ..components.order_component import OrderComponent


class OrdersPage(BasePage):
    TITLE = (By.XPATH, "//*[text()='Мои заказы']")
    NEW_ORDER_BTN = (By.ID, "orders-create-btn")
    COMMENT_ORDER = (By.XPATH, "//label[text()='Комментарий к заказу']//following::textarea[1]")
    INGREDIENTS_COMBOBOX = (By.XPATH, "//div[@role='combobox']")
    INGREDIENTS_LIST = (By.XPATH, "//li[contains(@data-testid, 'orders-ingredient-option')]")
    CANCEL_ORDER = (By.XPATH, "//button[@data-testid='orders-create-cancel-btn']")
    CREATE_ORDER = (By.XPATH, "//button[@data-testid='orders-create-confirm-btn']")
    ORDER_CARD_LIST = (By.XPATH, "//div[contains(@data-testid, 'order-card')]")
    DETAIL_DIALOG_CLOSE = (By.CSS_SELECTOR, "[data-testid='orders-detail-close-btn']")
    PAGINATION = (By.CSS_SELECTOR, "[data-testid='orders-pagination']")
    DELETE_ORDER_CONFIRM_BTN = (By.CSS_SELECTOR, "[data-testid='orders-delete-confirm-btn']")

    def get_orders(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='order-card-']")
        return [OrderComponent(card) for card in cards]

    def create_new_order(self, comment_order_text: str) -> 'OrdersPage':
        self.driver.find_element(*self.NEW_ORDER_BTN).click()
        self.driver.find_element(*self.INGREDIENTS_COMBOBOX).click()
        ingredients = self.driver.find_elements(*self.INGREDIENTS_LIST)
        if len(ingredients) >= 2:
            random.choice(ingredients).click()
            random.choice(ingredients).click()
        self.driver.find_element(*self.INGREDIENTS_COMBOBOX).click()
        self.driver.find_element(*self.COMMENT_ORDER).send_keys(comment_order_text)
        self.driver.find_element(*self.CREATE_ORDER).click()
        self.get_orders()
        return self

    def find_by_id(self, id_: str):
        selector = (By.CSS_SELECTOR, f"[data-testid='order-card-{id_}']")
        cards = self.driver.find_elements(*selector)
        return OrderComponent(cards[0]) if cards else None

    def find_by_comment(self, comment: str):
        for order in self.get_orders():
            if order.get_comment() == comment:
                return order
        return None

    def close_order_details_dialog(self) -> 'OrdersPage':
        self.driver.find_element(*self.DETAIL_DIALOG_CLOSE).click()
        return self

    def go_to_page(self, page: int) -> 'OrdersPage':
        btn = self.driver.find_element(By.CSS_SELECTOR, f"button[aria-label='Go to page {page}']")
        btn.click()
        return self

    def wait_for_page_loaded(self) -> 'OrdersPage':
        self.driver.find_element(*self.TITLE)
        self.driver.find_element(*self.NEW_ORDER_BTN)
        return self 