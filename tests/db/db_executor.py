import sqlite3
from typing import Any, List, Tuple, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Result
from typing import Any, List, Optional, Tuple

class DbExecutor:
    def __init__(self, db_url: str = "postgresql+psycopg2://coffee:coffee@localhost:5432/coffeehouse"):
        self.engine: Engine = create_engine(db_url)

    def execute(self, query: str, params: Optional[dict] = None) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    def fetchall(self, query: str, params: Optional[dict] = None) -> List[Tuple]:
        with self.engine.connect() as conn:
            result: Result = conn.execute(text(query), params or {})
            return result.fetchall()

    def fetchone(self, query: str, params: Optional[dict] = None) -> Optional[Tuple]:
        with self.engine.connect() as conn:
            result: Result = conn.execute(text(query), params or {})
            return result.fetchone()