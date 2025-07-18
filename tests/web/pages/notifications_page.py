from selenium.webdriver.common.by import By
from .base_page import BasePage
from ..components.notification_component import NotificationComponent


class NotificationsPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-testid='notifications-title']")
    MARK_ALL_AS_READ_BTN = (By.CSS_SELECTOR, "[data-testid='notifications-mark-all-read-btn']")
    DELETE_ALL_BTN = (By.CSS_SELECTOR, "[data-testid='notifications-delete-all-btn']")
    CONFIRM_BTN = (By.CSS_SELECTOR, "[data-testid='notifications-delete-confirm-btn']")
    CARDS = (By.CSS_SELECTOR, "[data-testid^='notification-card-']")

    def get_notifications(self):
        cards = self.driver.find_elements(*self.CARDS)
        return [NotificationComponent(card) for card in cards]

    def find_by_id(self, id_: str):
        selector = (By.CSS_SELECTOR, f"[data-testid='notification-card-{id_}']")
        cards = self.driver.find_elements(*selector)
        return NotificationComponent(cards[0]) if cards else None

    def find_by_message(self, message: str):
        for notification in self.get_notifications():
            if notification.get_message() == message:
                return notification
        return None

    def mark_all_as_read(self):
        self.driver.find_element(*self.MARK_ALL_AS_READ_BTN).click()

    def delete_all(self):
        self.driver.find_element(*self.DELETE_ALL_BTN).click()
        self.driver.find_element(*self.CONFIRM_BTN).click()

    def wait_for_page_loaded(self) -> 'NotificationsPage':
        self.driver.find_element(*self.TITLE)
        self.driver.find_element(*self.MARK_ALL_AS_READ_BTN)
        return self 