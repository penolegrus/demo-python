import pytest
from zeep import Client

from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto


class TestSoapOrders:
    @pytest.fixture(scope="module")
    def soap_client(self):
            return Client(wsdl="http://localhost:8080/ws/order.wsdl")

    def test_create_order_soap(self, soap_client, random_ingredient, random_user):
        generated_user = random_user(user_type="customer", create_new=True)
        response = soap_client.service.CreateOrder(
            userId=generated_user.user.id,
            ingredientIds=random_ingredient,
        )
        assert hasattr(response, "id")
        assert response.status == "CREATED"

    def test_get_order_by_id_soap(self, soap_client, random_user, random_ingredient, faker_instance):
        token = random_user().token
        order_client = OrderApiClient(token=token)

        body = CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_female())
        order = order_client.create_order(body)

        response = soap_client.service.Order(orderId=order.id)
        assert hasattr(response, "id")
        assert response.id == order.id


    def test_get_orders_by_user_soap(self, soap_client):
        for service in soap_client.wsdl.services.values():
            for port in service.ports.values():
                print(f"Service: {service.name}, Port: {port.name}")
                for op_name, operation in port.binding._operations.items():
                    print(f"  Operation: {op_name}")
                    print(f"    Input: {operation.input.signature()}")
                    print(f"    Output: {operation.output.signature()}")
