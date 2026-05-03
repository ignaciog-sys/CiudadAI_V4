import httpx

from config import settings
from schemas.api import CurrentUser, ItemsResponse, TokenResponse


class BackendApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def login(self, username: str, password: str) -> TokenResponse:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"username": username, "password": password},
            )
            response.raise_for_status()
            return TokenResponse(**response.json())

    async def me(self, token: str) -> CurrentUser:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return CurrentUser(**response.json())

    async def items(self, token: str) -> ItemsResponse:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.get(
                "/api/v1/items",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return ItemsResponse(**response.json())

    async def create_ticket(self, payload: dict) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            response = await client.post(
                "/api/v1/citizen/tickets",
                json=payload,
            )
            response.raise_for_status()
            return response.json()


api_client = BackendApiClient(settings.backend_base_url)
