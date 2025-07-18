from tests.rest.clients.base_client import HttpClient
from tests.rest.models.models import AuthRequest, RegisterRequest, AuthFullResponse, UserResponseDto


class AuthApiClient(HttpClient):
    def login(self, req: AuthRequest) -> AuthFullResponse:
        return self.post_("/api/auth/login", body=req, model=AuthFullResponse)

    def register(self, req: RegisterRequest) -> UserResponseDto:
        return self.post_("/api/auth/register", body=req, model=UserResponseDto)