from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class CurrentUser(BaseModel):
    username: str
    role: str


class Item(BaseModel):
    id: int
    name: str
    owner: str


class ItemsResponse(BaseModel):
    items: list[Item]
    requested_by: str | None = None
