import pytest

from tests.grpc.grpc_client import CoffeeOrderGrpcClient
from tests.rest.clients.ingredient_client import IngredientApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto, IngredientRequestDto


class TestCoffeeOrderGrpc:
    @pytest.fixture(scope="module")
    def grpc_client(self):
        return CoffeeOrderGrpcClient()

    def test_create_and_get_order(self, grpc_client, random_user, faker_instance):
        customer = random_user()

        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)
        body1 = IngredientRequestDto(name=faker_instance.unique.email(), quantity=faker_instance.random_int(10, 100))
        body2 = IngredientRequestDto(name=faker_instance.unique.email(), quantity=faker_instance.random_int(10, 100))
        ingredient1 = ingredient_client.create_ingredient(body1)
        ingredient2 = ingredient_client.create_ingredient(body2)

        # Создать заказ
        create_resp = grpc_client.create_order(user_id=customer.user.id, ingredient_ids=[ingredient1.id, ingredient2.id])
        assert create_resp.order.id
        order_id = create_resp.order.id

        # Получить заказ по id
        get_resp = grpc_client.get_order_by_id(order_id)
        assert get_resp.id == order_id

    def test_get_orders_by_user(self, grpc_client, random_user, faker_instance):
        customer = random_user()

        order_client = OrderApiClient(token=customer.token)
        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)

        body1 = IngredientRequestDto(name=faker_instance.unique.email(), quantity=faker_instance.random_int(10, 100))
        body2 = IngredientRequestDto(name=faker_instance.unique.email(), quantity=faker_instance.random_int(10, 100))
        ingredient1 = ingredient_client.create_ingredient(body1)
        ingredient2 = ingredient_client.create_ingredient(body2)

        order1 = CreateOrderDto(ingredientIds=[ingredient1.id], comment=faker_instance.name_male())
        order2 = CreateOrderDto(ingredientIds=[ingredient1.id, ingredient2.id], comment=faker_instance.name_male())

        order_client.create_order(order1)
        order_client.create_order(order2)

        resp = grpc_client.get_orders_by_user(user_id=customer.user.id)
        print(resp)

        orders = resp.orders
        assert len(orders) == 2

        assert hasattr(orders[0], "id")
        assert orders[0].userId == customer.user.id
        assert orders[0].status == "CREATED"
        assert hasattr(orders[0], "createdAt")
        assert ingredient1.id in orders[0].ingredientIds

        assert hasattr(orders[1], "id")
        assert orders[1].userId == customer.user.id
        assert orders[1].status == "CREATED"
        assert hasattr(orders[1], "createdAt")
        assert ingredient1.id, ingredient2.id in orders[1].ingredientIds

        order_ids = [order.id for order in orders]
        assert len(set(order_ids)) == len(order_ids)

#.\.venv\Scripts\activate
#python -m grpc_tools.protoc -I proto --python_out=grpc_gen --grpc_python_out=grpc_gen proto/coffee_order.proto