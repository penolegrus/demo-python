from typing import Optional
from .db_executor import DbExecutor

class UserRepository:
    def __init__(self, db_executor: DbExecutor):
        self.db = db_executor

    def get_by_id(self, user_id: int) -> Optional[dict]:
        row = self.db.fetchone("SELECT * FROM users WHERE id = :id", {"id": user_id})
        return dict(row) if row else None

    def get_by_username(self, username: str) -> Optional[dict]:
        row = self.db.fetchone("SELECT * FROM users WHERE username = :username", {"username": username})
        return dict(row) if row else None

    def create(self, username: str, email: str, password: str, role: str) -> int:
        self.db.execute(
            "INSERT INTO users (username, email, password, role) VALUES (:username, :email, :password, :role)",
            {"username": username, "email": email, "password": password, "role": role}
        )
        row = self.db.fetchone("SELECT id FROM users WHERE username = :username ORDER BY id DESC LIMIT 1", {"username": username})
        return row[0] if row else None

    def update_role_by_id(self, user_id: int, new_role: str) -> None:
        self.db.execute(
            "UPDATE users SET role = :role WHERE id = :id",
            {"role": new_role, "id": user_id}
        )

    def update_role_by_email(self, email: str, new_role: str) -> None:
        self.db.execute(
            "UPDATE users SET role = :role WHERE email = :email",
            {"role": new_role, "email": email}
        )