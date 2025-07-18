from __future__ import annotations

from tests.rest.clients.base_client import HttpClient
from tests.rest.models.models import CreateOrderDto, OrderResponse, UpdateOrderStatusRequest


class OrderApiClient(HttpClient):
    def get_order_by_id(self, order_id: int) -> OrderResponse:
        return self.get_(f"/api/orders/{order_id}", model=OrderResponse)

    def get_all_orders(self) -> list[OrderResponse]:
        return self.get_list_("/api/orders", model=OrderResponse)

    def get_pending_orders(self) -> list[OrderResponse]:
        return self.get_list_("/api/orders/pending", model=OrderResponse)

    def create_order(self, dto: CreateOrderDto) -> OrderResponse:
        return self.post_("/api/orders", body=dto, model=OrderResponse)

    def update_order_status(self, order_id: int, status: str) -> OrderResponse:
        return self.put_(f"/api/orders/{order_id}/status", body=UpdateOrderStatusRequest(status=status), model=OrderResponse)

    def delete_order_by_id(self, order_id: int) -> None:
        self.delete_(f"/api/orders/{order_id}")