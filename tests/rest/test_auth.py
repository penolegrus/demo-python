from tests.rest.models.models import AuthRequest, RegisterRequest

class TestAuth:

    def test_login_success(self, auth_client):
        req = AuthRequest(username="admin", password="admin")
        resp = auth_client.login(req)
        assert resp.token

    def test_register_success(self, auth_client, faker_instance):
        username = f"newuser_{faker_instance.unique.user_name()}"
        password = "123456"
        email = faker_instance.unique.email()
        req = RegisterRequest(username=username, email=email, password=password)
        resp = auth_client.register(req)
        assert resp.username == username 