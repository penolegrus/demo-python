from typing import List, Optional
import random
from .db_executor import DbExecutor

from typing import List
import random
from .db_executor import DbExecutor

class IngredientRepository:
    def __init__(self, db_executor: DbExecutor):
        self.db = db_executor

    def find_random_ids_with_positive_quantity(self, count: int) -> List[int]:
        rows = self.db.fetchall("SELECT id FROM ingredients WHERE quantity > 0")
        ids = [row[0] for row in rows]
        return random.sample(ids, min(count, len(ids)))

    def get_by_id(self, ingredient_id: int) -> Optional[dict]:
        row = self.db.fetchone("SELECT * FROM ingredients WHERE id = :id", {"id": ingredient_id})
        return dict(row) if row else None

    def create(self, name: str, quantity: int) -> int:
        self.db.execute(
            "INSERT INTO ingredients (name, quantity) VALUES (:name, :quantity)",
            {"name": name, "quantity": quantity}
        )
        row = self.db.fetchone("SELECT id FROM ingredients WHERE name = :name ORDER BY id DESC LIMIT 1", {"name": name})
        return row[0] if row else None

    def update_quantity(self, ingredient_id: int, quantity: int) -> None:
        self.db.execute(
            "UPDATE ingredients SET quantity = :quantity WHERE id = :id",
            {"quantity": quantity, "id": ingredient_id}
        )