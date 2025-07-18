import pytest
from typing import List

from tests.grpc.grpc_client import CoffeeOrderGrpcClient
from tests.rest.clients.ingredient_client import IngredientApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto, IngredientRequestDto


@pytest.fixture(scope="class")
def grpc_client() -> CoffeeOrderGrpcClient:
    return CoffeeOrderGrpcClient()


@pytest.fixture(scope="class")
def seller_token(random_user):
    return random_user(user_type="seller", create_new=True).token


@pytest.fixture(scope="class")
def ingredient_client(seller_token) -> IngredientApiClient:
    return IngredientApiClient(token=seller_token)


@pytest.fixture
def make_ingredients(ingredient_client, faker_instance):
    """Быстро создаёт N ингредиентов и возвращает их id."""
    def _create(count: int = 1) -> List[int]:
        ids = []
        for _ in range(count):
            body = IngredientRequestDto(
                name=faker_instance.unique.email(),
                quantity=faker_instance.random_int(10, 100)
            )
            ids.append(ingredient_client.create_ingredient(body).id)
        return ids
    return _create


class TestCoffeeOrderGrpc:
    def test_create_and_get_order(self, grpc_client, random_user, make_ingredients):
        customer = random_user()
        ingredient_ids = make_ingredients(2)

        create_resp = grpc_client.create_order(
            user_id=customer.user.id,
            ingredient_ids=ingredient_ids
        )
        assert create_resp.order.id

        fetched = grpc_client.get_order_by_id(create_resp.order.id)
        assert fetched.id == create_resp.order.id

    def test_get_orders_by_user(self, grpc_client, random_user, make_ingredients, faker_instance):
        customer = random_user()
        ingredient_ids = make_ingredients(2)

        order_client = OrderApiClient(token=customer.token)
        for subset in ([ingredient_ids[0]], ingredient_ids):
            order_client.create_order(
                CreateOrderDto(
                    ingredientIds=subset,
                    comment=faker_instance.name_male()
                )
            )

        orders = grpc_client.get_orders_by_user(user_id=customer.user.id).orders
        assert len(orders) == 2

        # общие проверки для всех заказов
        for order in orders:
            assert order.userId == customer.user.id
            assert order.status == "CREATED"
            assert hasattr(order, "id")
            assert hasattr(order, "createdAt")

        # конкретные проверки
        assert ingredient_ids[0] in orders[0].ingredientIds
        assert all(i in orders[1].ingredientIds for i in ingredient_ids)

        ids = [o.id for o in orders]
        assert len(set(ids)) == len(ids)  # уникальны