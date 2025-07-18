# tests/kafka/order_created_event.py
from dataclasses import dataclass
from typing import List

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