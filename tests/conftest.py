import os

import pytest
from faker import Faker
from selenium.webdriver.chrome import webdriver

from tests.db.db_executor import DbExecutor
from tests.db.ingredient_repository import IngredientRepository
from tests.rest.clients.auth_client import AuthApiClient
from tests.rest.models.models import AuthRequest, RegisterRequest, AuthFullResponse, CreateOrderDto

@pytest.fixture(scope="class")
def driver(request):
    """
    Создаём и передаём драйвер в каждый тест-класс.
    По умолчанию Chrome, но можно переопределить переменной окружения BROWSER.
    """
    drv = webdriver.Chrome()
    drv.implicitly_wait(10)
    request.cls.driver = drv  # доступен как self.driver внутри класса
    yield drv
    drv.quit()

@pytest.fixture(scope="class")
def base_ui_url():
    return os.getenv("BASE_URL", "http://localhost:5173")


@pytest.fixture
def faker_instance():
    return Faker()

@pytest.fixture
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

@pytest.fixture
def random_ingredient(ingredient_repository):
    return ingredient_repository.find_random_ids_with_positive_quantity(1)

@pytest.fixture
def auth_client() -> AuthApiClient:
    return AuthApiClient()

@pytest.fixture(scope="module")
def db_executor():
    return DbExecutor()

@pytest.fixture(scope="module")
def ingredient_repository(db_executor):
    return IngredientRepository(db_executor)

@pytest.fixture(scope="module")
def order_repository(db_executor):
    from tests.db.order_repository import OrderRepository
    return OrderRepository(db_executor)

@pytest.fixture(scope="module")
def user_repository(db_executor):
    from tests.db.user_repository import UserRepository
    return UserRepository(db_executor)