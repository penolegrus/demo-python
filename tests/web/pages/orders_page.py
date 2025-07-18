import time
from typing import Union, List, Optional

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from tests.web.pages.base_page import BasePage
from tests.web.components.order_component import OrderComponent
import random



class OrdersPage(BasePage):
    TITLE        = (By.XPATH, "//*[text()='Мои заказы']")
    NEW_ORDER    = (By.ID, "orders-create-btn")
    COMMENT      = (By.XPATH, "//label[text()='Комментарий к заказу']//following::textarea[1]")
    COMBO        = (By.XPATH, "//div[@role='combobox']")
    OPTIONS      = (By.XPATH, "//li[contains(@data-testid, 'orders-ingredient-option')]")
    CREATE       = (By.XPATH, "//button[@data-testid='orders-create-confirm-btn']")
    CARD         = (By.CSS_SELECTOR, "[data-testid^='order-card-']")

    # ----- общие методы -----
    def open(self, base_url: str) -> "OrdersPage":
        super().open(base_url)
        return self.wait_loaded()

    def wait_loaded(self) -> "OrdersPage":
        self.is_visible(*self.TITLE)
        self.is_visible(*self.NEW_ORDER)
        return self

    @property
    def orders(self) -> list[OrderComponent]:
        return [OrderComponent(el) for el in self.driver.find_elements(*self.CARD)]

    def order_by_comment(self, comment: str) -> Optional[OrderComponent]:
        return next((o for o in self.orders if o.comment == comment), None)

    def order_by_id(self, id_: str) -> Optional[OrderComponent]:
        selector = (By.CSS_SELECTOR, f"[data-testid='order-card-{id_}']")
        el = self.driver.find_elements(*selector)
        return OrderComponent(el[0]) if el else None

    # ----- создание заказа -----
    def create_order(self, comment: str) -> "OrdersPage":
        self.click(*self.NEW_ORDER)
        self.click(*self.COMBO)

        options = self.driver.find_elements(*self.OPTIONS)
        if len(options) >= 2:
            random.choice(options).click()
            random.choice(options).click()

        self.actions.send_keys(Keys.ESCAPE).perform()
        self.fill(*self.COMMENT, text=comment)
        self.click(*self.CREATE)

        time.sleep(1)
        return self