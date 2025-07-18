import grpc

from grpc_gen import coffee_order_pb2_grpc, coffee_order_pb2


class CoffeeOrderGrpcClient:
    def __init__(self, host="localhost", port=9090):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = coffee_order_pb2_grpc.CoffeeOrderServiceStub(self.channel)

    def get_order_by_id(self, order_id: int):
        request = coffee_order_pb2.CoffeeOrderRequest(id=order_id)
        return self.stub.GetOrderById(request)

    def get_orders_by_user(self, user_id: int):
        request = coffee_order_pb2.UserOrdersRequest(userId=user_id)
        return self.stub.GetOrdersByUser(request)

    def create_order(self, user_id: int, ingredient_ids: list):
        request = coffee_order_pb2.CreateCoffeeOrderRequest(
            userId=user_id,
            ingredientIds=ingredient_ids
        )
        return self.stub.CreateOrder(request)