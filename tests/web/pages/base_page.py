# tests/web/pages/base_page.py
from __future__ import annotations

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_WAIT = 15

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_WAIT)
        self.actions = ActionChains(driver)

    # ----- самые частые действия -----
    def open(self, url: str) -> None:
        self.driver.get(url)

    def fill(self, by: By, value: str, *, text: str) -> None:
        el = self.wait.until(EC.element_to_be_clickable((by, value)))
        el.clear()
        el.send_keys(text)

    def click(self, by: By, value: str) -> None:
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def text(self, by: By, value: str) -> str:
        return self.wait.until(EC.visibility_of_element_located((by, value))).text

    def is_visible(self, by: By, value: str) -> bool:
        return bool(self.wait.until(EC.visibility_of_element_located((by, value))))