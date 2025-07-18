import pytest
from zeep import Client

from tests.rest.clients.order_client import OrderApiClient
from tests.rest.models.models import CreateOrderDto


@pytest.fixture(scope="module")
def soap_client():
    return Client(wsdl="http://localhost:8080/ws/order.wsdl")

class TestSoapOrders:

    def test_create_order(self, soap_client, random_user, random_ingredient):
        order = soap_client.service.CreateOrder(userId=random_user().user.id, ingredientIds=random_ingredient)
        assert order.id
        assert order.status == "CREATED"

    def test_get_order_by_id(self, soap_client, random_user, random_ingredient, faker_instance):
        token = random_user().token
        order = OrderApiClient(token=token).create_order(
            CreateOrderDto(ingredientIds=random_ingredient, comment=faker_instance.name_female())
        )
        fetched = soap_client.service.Order(orderId=order.id)
        assert fetched.id == order.id

    def test_list_services(self, soap_client):
        """Utility: print WSDL structure."""
        for service in soap_client.wsdl.services.values():
            for port in service.ports.values():
                print(f"Service: {service.name}, Port: {port.name}")
                for op_name, op in port.binding._operations.items():
                    print(f"  Operation: {op_name}")
                    print(f"    Input: {op.input.signature()}")
                    print(f"    Output: {op.output.signature()}")