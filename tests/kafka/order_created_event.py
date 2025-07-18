# tests/kafka/order_created_event.py
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OrderCreatedEvent:
    orderId: int
    userId: int
    ingredientIds: List[int]
    status: str

    def __init__(self, orderId, userId, ingredientIds, status, **kwargs):
        self.orderId = orderId
        self.userId = userId
        self.ingredientIds = ingredientIds
        self.status = status

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderCreatedEvent":
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
