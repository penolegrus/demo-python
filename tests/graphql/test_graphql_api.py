import pytest
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from faker import Faker

GRAPHQL_URL = "http://localhost:8080/graphql"  # Измените на ваш адрес

@pytest.fixture(scope="module")
def gql_client():
    transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client

class TestGraphQLApi:
    def test_ingredients_query(self, gql_client):
        query = gql("""
            query {
              ingredients {
                id
                name
                quantity
              }
            }
        """)
        result = gql_client.execute(query)
        assert "ingredients" in result

    def test_create_ingredient_mutation(self, gql_client, faker_instance):
        query = gql("""
            mutation CreateIngredient($name: String!, $quantity: Int!) {
              createIngredient(name: $name, quantity: $quantity) {
                id
                name
                quantity
              }
            }
        """)
        variables = {"name": faker_instance.unique.word(), "quantity": 42}
        result = gql_client.execute(query, variable_values=variables)
        assert "createIngredient" in result
        assert result["createIngredient"]["quantity"] == 42

    def test_create_user_mutation(self, gql_client, faker_instance):
        query = gql("""
            mutation CreateUser($username: String!, $email: String!, $password: String!, $role: String!) {
              createUser(username: $username, email: $email, password: $password, role: $role) {
                id
                username
                email
                role
              }
            }
        """)
        variables = {
            "username": faker_instance.unique.user_name(),
            "email": faker_instance.unique.email(),
            "password": "123456",
            "role": "CUSTOMER"
        }
        result = gql_client.execute(query, variable_values=variables)
        assert "createUser" in result
        assert result["createUser"]["role"] == "CUSTOMER"

    def test_get_users_query(self, gql_client):
        query = gql("""
            query {
                users {
                    id
                    username
                    email
                    role
                }
            }
        """)
        result = gql_client.execute(query)
        assert "users" in result

    def test_users_by_role_query(self, gql_client):
        query = gql("""
            query UsersByRole($role: Role!) {
              users(role: $role) {
                id
                username
                email
                role
              }
            }
        """)
        variables = {"role": "CUSTOMER"}
        result = gql_client.execute(query, variable_values=variables)
        assert "users" in result

    def test_create_order_mutation(self, gql_client):
        query = gql("""
            mutation CreateOrder($userId: ID!, $ingredientIds: [ID!]!) {
              createOrder(userId: $userId, ingredientIds: $ingredientIds) {
                id
                status
                createdAt
                user { id username }
                ingredients { id name quantity }
              }
            }
        """)
        # Здесь userId и ingredientIds должны быть валидными!
        variables = {"userId": 1, "ingredientIds": [1, 2]}
        result = gql_client.execute(query, variable_values=variables)
        assert "createOrder" in result

    def test_orders_by_status_query(self, gql_client):
        query = gql("""
            query OrdersByStatus($status: CoffeeOrderStatus!) {
              orders(status: $status) {
                id
                user { id username }
                ingredients { id name quantity }
                createdAt
                status
              }
            }
        """)
        variables = {"status": "CREATED"}
        result = gql_client.execute(query, variable_values=variables)
        assert "orders" in result

    def test_messages_query(self, gql_client):
        query = gql("""
            query Messages($senderId: ID!, $receiverId: ID!) {
              messages(senderId: $senderId, receiverId: $receiverId) {
                id
                sender { id username }
                receiver { id username }
                content
                sentAt
              }
            }
        """)
        variables = {"senderId": 1, "receiverId": 2}
        result = gql_client.execute(query, variable_values=variables)
        assert "messages" in result 