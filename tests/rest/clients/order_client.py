from .rest_client import RestClient
from tests.rest.models.models import OrderResponse, CreateOrderDto, UpdateOrderStatusRequest
from typing import List, Optional

class OrderApiClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None):
        self.rest = RestClient(base_url, token)

    def get_order_by_id(self, order_id: int) -> OrderResponse:
        return self.rest.get(f"/api/orders/{order_id}", OrderResponse)

    def delete_order_by_id(self, order_id: int):
        return self.rest.delete(f"/api/orders/{order_id}")

    def get_all_orders(self) -> List[OrderResponse]:
        return self.rest.get_list("/api/orders", OrderResponse, paginated=True)

    def get_pending_orders(self) -> List[OrderResponse]:
        return self.rest.get_list("/api/orders/pending", OrderResponse, paginated=True)

    def create_order(self, dto: CreateOrderDto) -> OrderResponse:
        return self.rest.post("/api/orders", dto.dict(), OrderResponse)

    def update_order_status(self, order_id: int, status: str) -> OrderResponse:
        req = UpdateOrderStatusRequest(status=status)
        return self.rest.put(f"/api/orders/{order_id}/status", req.dict(), OrderResponse) 