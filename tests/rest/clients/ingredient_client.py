from .rest_client import RestClient
from tests.rest.models.models import IngredientRequestDto, IngredientResponseDto
from typing import List, Optional

class IngredientApiClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None):
        self.rest = RestClient(base_url, token)

    def get_all_ingredients(self) -> List[IngredientResponseDto]:
        return self.rest.get_list("/api/ingredients", IngredientResponseDto)

    def get_available_ingredients(self) -> List[IngredientResponseDto]:
        return self.rest.get_list("/api/ingredients/available", IngredientResponseDto)

    def create_ingredient(self, dto: IngredientRequestDto) -> IngredientResponseDto:
        return self.rest.post("/api/ingredients", dto.dict(), IngredientResponseDto)

    def update_ingredient(self, ingredient_id: int, dto: IngredientRequestDto) -> IngredientResponseDto:
        return self.rest.put(f"/api/ingredients/{ingredient_id}", dto.dict(), IngredientResponseDto)

    def delete_ingredient(self, ingredient_id: int):
        return self.rest.delete(f"/api/ingredients/{ingredient_id}") 