from .rest_client import RestClient
from tests.rest.models.models import AuthRequest, RegisterRequest, AuthFullResponse, UserResponseDto


class AuthApiClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.rest = RestClient(base_url)

    def login(self, req: AuthRequest) -> AuthFullResponse:
        return self.rest.post("/api/auth/login", req.dict(), AuthFullResponse)

    def register(self, req: RegisterRequest) -> UserResponseDto:
        return self.rest.post("/api/auth/register", req.dict(), UserResponseDto) 