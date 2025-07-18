from .base_client import HttpClient
from tests.rest.models.models import IngredientRequestDto, IngredientResponseDto


class IngredientApiClient(HttpClient):
    def get_all_ingredients(self) -> list[IngredientResponseDto]:
        return self.get_list_("/api/ingredients", model=IngredientResponseDto)

    def get_available_ingredients(self) -> list[IngredientResponseDto]:
        return self.get_list_("/api/ingredients/available", model=IngredientResponseDto)

    def create_ingredient(self, dto: IngredientRequestDto) -> IngredientResponseDto:
        return self.post_("/api/ingredients", body=dto, model=IngredientResponseDto)

    def update_ingredient(self, ingredient_id: int, dto: IngredientRequestDto) -> IngredientResponseDto:
        return self.put_(f"/api/ingredients/{ingredient_id}", body=dto, model=IngredientResponseDto)

    def delete_ingredient(self, ingredient_id: int) -> None:
        self.delete_(f"/api/ingredients/{ingredient_id}")