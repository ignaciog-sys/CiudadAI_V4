# Plantilla base profesional de FastAPI

Esta carpeta es un punto de partida limpio para equipos de bootcamp que ya iniciaron un proyecto y quieren ordenar su backend con una estructura mantenible.

La base está inspirada en patrones reales de APIs productivas: app central, configuración por entorno, routers por dominio, dependencias de seguridad, capa de servicios y pruebas desde el inicio.

## Qué incluye

- arranque de FastAPI con lifespan y handlers globales de error
- configuración centralizada con Pydantic Settings
- autenticación básica estilo OAuth2 Bearer (mock, reemplazable)
- separación clara entre router, servicio y modelos
- documentación OpenAPI automática
- tests base con pytest y TestClient

## Estructura del repositorio

```text
fastapi-base-template/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── pyproject.toml
├── requirements.txt
├── dev-requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   ├── deps.py
│   ├── middleware.py
│   ├── spec.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── responses.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── errors.py
│   │   └── health.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   ├── health_router.py
│   │   ├── items_router.py
│   │   └── router_template.py
│   └── services/
│       ├── __init__.py
│       └── auth_service.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    └── test_health.py
```

## Librerías mínimas

Dependencias de ejecución:

- fastapi
- uvicorn
- pydantic-settings

Dependencias de desarrollo:

- pytest
- httpx
- ruff

## Qué es pyproject.toml

pyproject.toml es el archivo estándar de configuración del proyecto Python. En esta plantilla centraliza:

- metadatos del proyecto (nombre, versión, python requerido)
- dependencias principales
- configuración de herramientas (pytest y ruff)

Tener esto en un único archivo ayuda a mantener consistencia entre equipos y entornos CI/CD.

## Ejecución local

1. Crear entorno virtual e instalar dependencias:

```bash
python -m pip install -r requirements.txt
python -m pip install -r dev-requirements.txt
```

2. Copiar .env.example a .env y ajustar valores mínimos.
3. Ejecutar la API:

```bash
uvicorn src.app:app --reload
```

4. Abrir documentación:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Ejecución con Docker

```bash
docker compose up --build
```

La API quedará publicada en http://127.0.0.1:8000.

## Autenticación incluida (base)

La plantilla implementa una versión mínima del patrón OAuth2 Bearer:

- POST /api/v1/auth/login valida credenciales mock y entrega token bearer.
- OAuth2PasswordBearer extrae el token del header Authorization.
- get_current_user valida el token y construye el usuario actual.
- endpoints como /api/v1/items quedan protegidos por dependencia.

Esto está diseñado para reemplazarse fácilmente por autenticación real:

1. JWT firmados por el propio backend.
2. Keycloak, Auth0 o proveedor OIDC externo.
3. IdP corporativo con introspección o JWKS.

## Cómo adaptar esta base a un proyecto real

- Mantener routers centrados en HTTP (validación y respuestas), no en lógica de negocio.
- Mover reglas de negocio a services para facilitar testing y reutilización.
- Definir contratos de entrada y salida en models.
- Reutilizar dependencias en deps para seguridad, contexto de usuario y recursos comunes.
- Si aparece persistencia, crear src/db con sesión, repositorios y modelos ORM.
- Si hay integraciones externas, crear src/clients o src/integrations por proveedor.
- Si hay requisitos de seguridad adicionales, extender middlewares y handlers en lugar de dispersar lógica en cada endpoint.

## Decisiones de diseño de esta plantilla

- No incluye base de datos por defecto para reducir complejidad inicial.
- Incluye seguridad mínima para exponer el patrón de autenticación desde el inicio.
- Evita dependencias corporativas o acoplamientos propietarios.
- Cada archivo incluye contexto breve en español para acelerar adopción por equipos.

## Hallazgos estructurales tomados de proyectos reales

Del análisis profundo de implementaciones similares se abstrajeron estas decisiones:

- centralizar configuración y no leer variables de entorno desde routers
- usar dependencia de usuario actual en endpoints protegidos
- separar validaciones y regex de negocio fuera de handlers
- definir respuestas de error comunes para mantener contratos homogéneos
- trabajar con tests que verifiquen seguridad, no solo casos felices
- reservar un archivo de especificación (src/spec.py) para metadatos OpenAPI si el proyecto crece

## Comandos de trabajo útiles

```bash
# Ejecutar tests
pytest -q

# Ejecutar lint
ruff check .

# Formatear
ruff format .
```

## Limitaciones intencionales

Esta plantilla no intenta imponer una arquitectura cerrada. Es una base limpia para integrar equipos, estandarizar estructura y evolucionar el proyecto sin deuda temprana.