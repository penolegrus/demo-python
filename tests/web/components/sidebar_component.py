from selenium.webdriver.common.by import By
from tests.web.pages.base_page import BasePage
from tests.web.pages.pending_orders_page import PendingOrdersPage


class SideBarComponent(BasePage):
    MY_ORDERS_BTN = (By.XPATH, "//*[text()='Мои заказы']")
    PENDING_ORDERS_BTN = (By.XPATH, "//*[text()='Заказы']")
    INGREDIENTS_BTN = (By.XPATH, "//*[text()='Ингредиенты']")
    USERS_BTN = (By.XPATH, "//*[text()='Пользователи']")
    CHAT_BTN = (By.XPATH, "//*[text()='Чат']")
    GRAPHQL_BTN = (By.XPATH, "//*[text()='GraphQL']")
    GRPC_PROXY_BTN = (By.XPATH, "//*[text()='gRPC Proxy']")
    SOAP_PROXY_BTN = (By.XPATH, "//*[text()='SOAP Proxy']")
    KAFKA_BTN = (By.XPATH, "//*[text()='Kafka']")
    NOTIFICATION_BTN = (By.XPATH, "//*[text()='Уведомления']")
    LOGOUT_BTN = (By.XPATH, "//*[text()='Выход']")
    UNREAD_NOTIFICATION_COUNT = (By.CSS_SELECTOR, "[data-testid='notifications-unread-count']")

    def go_to_pending_orders_page(self) -> PendingOrdersPage:
        self.driver.find_element(*self.PENDING_ORDERS_BTN).click()
        return PendingOrdersPage(self.driver)

    def go_to_notification_page(self):
        self.driver.find_element(*self.NOTIFICATION_BTN).click()

    def go_to_orders_page(self):
        self.driver.find_element(*self.MY_ORDERS_BTN).click()

    def get_unread_notification_count(self) -> str:
        return self.driver.find_element(*self.UNREAD_NOTIFICATION_COUNT).text

    def log_out(self):
        return self.driver.find_element(*self.LOGOUT_BTN).click()