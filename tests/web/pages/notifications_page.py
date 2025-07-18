from selenium.webdriver.common.by import By
from tests.web.pages.base_page import BasePage
from tests.web.components.notification_component import NotificationComponent
from typing import List, Optional


class NotificationsPage(BasePage):
    TITLE       = (By.CSS_SELECTOR, "[data-testid='notifications-title']")
    MARK_READ   = (By.CSS_SELECTOR, "[data-testid='notifications-mark-all-read-btn']")
    DELETE_ALL  = (By.CSS_SELECTOR, "[data-testid='notifications-delete-all-btn']")
    CONFIRM     = (By.CSS_SELECTOR, "[data-testid='notifications-delete-confirm-btn']")
    CARD        = (By.CSS_SELECTOR, "[data-testid^='notification-card-']")

    def open(self, base_url: str) -> "NotificationsPage":
        super().open(base_url)
        return self.wait_loaded()

    def wait_loaded(self) -> "NotificationsPage":
        self.is_visible(*self.TITLE)
        self.is_visible(*self.MARK_READ)
        return self

    @property
    def notifications(self) -> List[NotificationComponent]:
        return [NotificationComponent(el) for el in self.driver.find_elements(*self.CARD)]

    def notification_by_id(self, id_: str) -> Optional[NotificationComponent]:
        selector = (By.CSS_SELECTOR, f"[data-testid='notification-card-{id_}']")
        els = self.driver.find_elements(*selector)
        return NotificationComponent(els[0]) if els else None

    def notification_by_message(self, message: str) -> Optional[NotificationComponent]:
        return next((n for n in self.notifications if n.message == message), None)

    def mark_all_read(self) -> None:
        self.click(*self.MARK_READ)

    def clear_all(self) -> None:
        self.click(*self.DELETE_ALL)
        self.click(*self.CONFIRM)