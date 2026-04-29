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

    async def crear_ticket(
        self,
        token: str,
        titulo: str,
        descripcion: str,
        ubicacion: str,
        categoria_sugerida: str,
    ) -> dict | None:
        """Crear un ticket en el backend usando token Bearer."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.post(
                    "/api/tickets",
                    json={
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "ubicacion": ubicacion,
                        "categoria_sugerida": categoria_sugerida,
                    },
                    headers={"Authorization": f"Bearer {token}"},
                )
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                return None
            except (httpx.HTTPStatusError, httpx.RequestError):
                return None

    async def obtener_ticket(self, ticket_id: str) -> dict | None:
        """Obtener un ticket por ID sin autenticación."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.get(f"/api/tickets/{ticket_id}")
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                return None
            except (httpx.HTTPStatusError, httpx.RequestError):
                return None

    async def listar_tickets_worker(self, token: str) -> list | None:
        """Listar tickets para el trabajador con token Bearer."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.get(
                    "/api/worker/tickets",
                    headers={"Authorization": f"Bearer {token}"},
                )
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                return None
            except (httpx.HTTPStatusError, httpx.RequestError):
                return None

    async def actualizar_ticket(
        self,
        token: str,
        ticket_id: str,
        estado: str,
        respuesta: str,
    ) -> dict | None:
        """Actualizar el estado y respuesta de un ticket con token Bearer."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.put(
                    f"/api/worker/tickets/{ticket_id}",
                    json={"estado": estado, "respuesta": respuesta},
                    headers={"Authorization": f"Bearer {token}"},
                )
                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                return None
            except (httpx.HTTPStatusError, httpx.RequestError):
                return None


api_client = BackendApiClient(settings.backend_base_url)
