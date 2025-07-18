import pytest

from tests.rest.models.models import AuthRequest, RegisterRequest

@pytest.mark.usefixtures("auth_client", "faker_instance")
class TestAuthV2:

    def test_login(self, auth_client):
        assert auth_client.login(AuthRequest(username="admin", password="admin")).token

    def test_register(self, auth_client, faker_instance):
        req = RegisterRequest(
            username=faker_instance.unique.user_name(),
            email=faker_instance.unique.email(),
            password="123456"
        )
        created = auth_client.register(req)
        assert created.username == req.username