from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url: str):
        self.driver.get(url)

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))