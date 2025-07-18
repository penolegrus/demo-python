# tests/web/components/base_component.py
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple

Locator = Tuple[By, str]


class BaseComponent:
    """Минимальный каркас любого компонента."""
    def __init__(self, root: WebElement):
        self.root = root

    def _text(self, locator: Locator) -> str:
        return self.root.find_element(*locator).text

    def _attr(self, locator: Locator, attr: str) -> str:
        return self.root.find_element(*locator).get_attribute(attr)