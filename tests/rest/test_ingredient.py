from datetime import datetime

import pytest

from tests.rest.clients.ingredient_client import IngredientApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import IngredientRequestDto, CreateOrderDto

@pytest.mark.usefixtures("ingredient_client", "customer_client")
class TestIngredient:
    def test_create_list_delete(self, ingredient_client, faker):
        body = IngredientRequestDto(name=str(datetime.now().microsecond), quantity=faker.random_int(10, 100))
        ing = ingredient_client.create_ingredient(body)

        assert next(i for i in ingredient_client.get_all_ingredients() if i.id == ing.id)

        ingredient_client.delete_ingredient(ing.id)
        assert not any(i.id == ing.id for i in ingredient_client.get_all_ingredients())

    def test_edit(self, ingredient_client, faker):
        body = IngredientRequestDto(name=faker.email(), quantity=100)
        response = ingredient_client.create_ingredient(body)

        body.quantity = 1
        updated = ingredient_client.update_ingredient(response.id, body)
        assert updated.quantity == 1

    def test_quantity_decreases_on_order(self, ingredient_client, customer_client, faker):
        body = IngredientRequestDto(name=str(datetime.now().microsecond), quantity=1)
        ing = ingredient_client.create_ingredient(body)

        before = ingredient_client.get_available_ingredients()

        customer_client.create_order(CreateOrderDto(ingredientIds=[ing.id], comment=faker.word()))

        after = ingredient_client.get_available_ingredients()

        assert before != after