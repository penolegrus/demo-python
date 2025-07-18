from tests.rest.clients.ingredient_client import IngredientApiClient
from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import IngredientRequestDto, CreateOrderDto

class TestIngredient:
    def test_create_and_get_ingredient(self, random_user, random_ingredient, faker_instance):
        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)

        body = IngredientRequestDto(name=faker_instance.unique.word(), quantity=faker_instance.random_int(10, 100))

        ingredient = ingredient_client.create_ingredient(body)
        all_ingredients = ingredient_client.get_all_ingredients()
        assert all_ingredients

        created = next((ing for ing in all_ingredients if ing.name == ingredient.name), None)
        assert created is not None
        assert created.id == ingredient.id
        assert created.quantity == ingredient.quantity
        assert created.name == ingredient.name

    def test_delete_ingredient(self, random_user, faker_instance):
        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)

        body = IngredientRequestDto(name=faker_instance.unique.word(), quantity=faker_instance.random_int(10, 100))

        ingredient = ingredient_client.create_ingredient(body)

        resp = ingredient_client.delete_ingredient(ingredient.id)
        assert resp.status_code == 204

    def test_edit_ingredient(self, random_user, faker_instance):
        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)

        body = IngredientRequestDto(name=faker_instance.unique.word(), quantity=faker_instance.random_int(10, 100))

        ingredient = ingredient_client.create_ingredient(body)
        body.quantity = 1
        updated = ingredient_client.update_ingredient(ingredient.id, body)
        assert updated.quantity == body.quantity
        assert updated.name == body.name

    def test_available_ingredients_spends(self, random_user, faker_instance):
        ingredient_client = IngredientApiClient(token=random_user(user_type="seller").token)
        order_client = OrderApiClient(token=random_user(user_type="customer").token)

        body = IngredientRequestDto(name=faker_instance.unique.word(), quantity=1)
        ingredient = ingredient_client.create_ingredient(body)

        available_before = ingredient_client.get_available_ingredients()
        order = CreateOrderDto(ingredientIds=[ingredient.id], comment=faker_instance.unique.word())
        order_client.create_order(order)

        available_after = ingredient_client.get_available_ingredients()
        assert available_before != available_after