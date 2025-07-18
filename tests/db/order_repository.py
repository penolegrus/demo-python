# tests/db/order_repository.py
from typing import List, Optional
from .db_executor import DbExecutor

class OrderRepository:
    def __init__(self, db_executor: DbExecutor):
        self.db = db_executor

    def get_by_id(self, order_id: int) -> Optional[dict]:
        row = self.db.fetchone("SELECT * FROM orders WHERE id = :id", {"id": order_id})
        return dict(row) if row else None

    def get_all_by_user(self, user_id: int) -> List[dict]:
        rows = self.db.fetchall("SELECT * FROM orders WHERE user_id = :user_id", {"user_id": user_id})
        return [dict(row) for row in rows]

    def create(self, user_id: int, comment: str, status: str = 'NEW') -> int:
        self.db.execute(
            "INSERT INTO orders (user_id, comment, status) VALUES (:user_id, :comment, :status)",
            {"user_id": user_id, "comment": comment, "status": status}
        )
        row = self.db.fetchone("SELECT id FROM orders WHERE user_id = :user_id ORDER BY id DESC LIMIT 1", {"user_id": user_id})
        return row[0] if row else None

    def update_status(self, order_id: int, status: str) -> None:
        self.db.execute(
            "UPDATE orders SET status = :status WHERE id = :id",
            {"status": status, "id": order_id}
        )