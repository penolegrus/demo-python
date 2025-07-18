import os
import time

import pytest
from faker import Faker
from selenium import webdriver

from tests.db.db_executor import DbExecutor
from tests.db.ingredient_repository import IngredientRepository
from tests.rest.clients.auth_client import AuthApiClient
from tests.rest.clients.ingredient_client import IngredientApiClient
from tests.rest.clients.notification_client import NotificationApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import AuthRequest, RegisterRequest, AuthFullResponse, CreateOrderDto

@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    # Отключить менеджер паролей и проверку паролей
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-blink-features=PasswordManagerIntegration")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="class")
def base_ui_url():
    return os.getenv("BASE_URL", "http://localhost:5173")

@pytest.fixture(scope="class")
def faker_instance():
    return Faker()

@pytest.fixture(scope="class")
def random_user(auth_client, faker_instance, user_repository):
    def _get_token(user_type: str = "customer", create_new: bool = True) -> AuthFullResponse:
        if create_new:
            email = faker_instance.ascii_free_email()
            username = f"{user_type}_{faker_instance.unique.ascii_free_email()}"
            password = user_type
            req = RegisterRequest(email=email, username=username, password=password)
            response = auth_client.register(req)
            user_repository.update_role_by_id(response.id, user_type.upper())
        else:
            # Используем дефолтного пользователя (должен быть создан заранее)
            username = user_type
            password = user_type

        login_request = AuthRequest(username=username, password=password)
        return auth_client.login(login_request)
    return _get_token

@pytest.fixture(scope="class")
def random_ingredient(ingredient_repository):
    return ingredient_repository.find_random_ids_with_positive_quantity(1)

@pytest.fixture(scope="class")
def auth_client() -> AuthApiClient:
    return AuthApiClient()

@pytest.fixture(scope="class")
def db_executor():
    return DbExecutor()

@pytest.fixture(scope="class")
def ingredient_repository(db_executor):
    return IngredientRepository(db_executor)

@pytest.fixture(scope="class")
def order_repository(db_executor):
    from tests.db.order_repository import OrderRepository
    return OrderRepository(db_executor)

@pytest.fixture(scope="class")
def user_repository(db_executor):
    from tests.db.user_repository import UserRepository
    return UserRepository(db_executor)




@pytest.fixture(scope="class")
def seller_client(random_user) -> OrderApiClient:
    return OrderApiClient(token=random_user(user_type="seller").token)

@pytest.fixture(scope="class")
def customer_client(random_user) -> OrderApiClient:
    return OrderApiClient(token=random_user(user_type="customer").token)

@pytest.fixture(scope="class")
def ingredient_client(random_user) -> IngredientApiClient:
    return IngredientApiClient(token=random_user(user_type="seller").token)

@pytest.fixture(scope="class")
def notification_client(random_user) -> NotificationApiClient:
    return NotificationApiClient(token=random_user(user_type="seller").token)


def poll_until(predicate, *, timeout=5, step=0.5):
    end = time.time() + timeout
    while time.time() < end:
        result = predicate()
        if result:
            return result
        time.sleep(step)
    return None