"""Configuración central de la aplicación.

Propósito: leer variables de entorno con Pydantic Settings y ofrecer un objeto único de configuración.
Ejemplo de uso: importar settings desde cualquier módulo para evitar valores hardcoded.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src import __description__, __title__, __version__


class Settings(BaseSettings):
    """Valores de configuración de la API.

    Esta clase carga opciones desde .env y permite cambiar comportamiento sin tocar código.
    """

    # extra=ignore permite que el .env tenga variables adicionales sin romper la carga.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default=__title__, alias="APP_NAME")
    app_version: str = Field(default=__version__, alias="APP_VERSION")
    app_description: str = Field(default=__description__, alias="APP_DESCRIPTION")
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    docs_url: str | None = Field(default="/docs", alias="DOCS_URL")
    openapi_url: str | None = Field(default="/openapi.json", alias="OPENAPI_URL")
    redoc_url: str | None = Field(default="/redoc", alias="REDOC_URL")
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    # Parámetros mock para bootstrap de seguridad básica.
    mock_auth_username: str = Field(default="api_user", alias="MOCK_AUTH_USERNAME")
    mock_auth_password: str = Field(default="change_me", alias="MOCK_AUTH_PASSWORD")
    mock_auth_token: str = Field(default="bootstrap-token", alias="MOCK_AUTH_TOKEN")


settings = Settings()