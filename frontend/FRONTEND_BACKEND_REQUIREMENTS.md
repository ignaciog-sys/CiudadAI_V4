# Cambios en el frontend y requisitos del backend

## Cambios realizados en el frontend

### 1. `frontend/services/api_client.py`
- Se amplió el cliente HTTP para incluir métodos de tickets:
  - `crear_ticket(token, titulo, descripcion, ubicacion, categoria_sugerida)`
  - `obtener_ticket(ticket_id)`
  - `listar_tickets_worker(token)`
  - `actualizar_ticket(token, ticket_id, estado, respuesta)`
- Todos los métodos usan `httpx.AsyncClient` y envían el token con `Authorization: Bearer {token}`.
- Manejan errores de conexión/respuesta devolviendo `None` cuando la petición no es 2xx o falla.

### 2. `frontend/routes/pages.py`
- Se añadieron nuevas rutas frontend para exponer la lógica de tickets:
  - `POST /citizen/tickets`
  - `GET /citizen/tickets/{ticket_id}`
  - `GET /admin/tickets`
  - `PUT /admin/tickets/{ticket_id}`
- Se implementó verificación de rol en la sesión:
  - rutas `/citizen/*` solo para `citizen`
  - rutas `/admin/*` solo para `admin`
- Las rutas usan el cliente `api_client` para llamar al backend y devuelven JSON adecuado.

### 3. `frontend/templates/citizen_dashboard.html`
- Se añadió un formulario interactivo de creación de ticket con campos:
  - Título
  - Descripción
  - Ubicación
  - Categoría sugerida
- Se añadió un buscador de ticket por ID con resultados mostrados en la misma página.
- Toda la interacción usa `fetch()` y no recarga la página.
- Se muestran mensajes de estado, carga y error.
- Se mantuvo el tema verde del panel ciudadano.

### 4. `frontend/templates/admin_dashboard.html`
- Se añadió carga dinámica de tickets al abrir el panel admin desde `/admin/tickets`.
- Se agregó una tabla con columnas:
  - ID
  - Título
  - Urgencia
  - Estado
  - Acción
- Se ordena visualmente por urgencia (`alta` → `media` → `baja`).
- Se añadieron badges de color para urgencia: rojo, naranja, verde.
- Se añadió gestión inline de cada ticket con:
  - select de estado (`nuevo`, `pendiente`, `cerrado`)
  - textarea de respuesta municipal
  - botón `Guardar cambios`
- La actualización del ticket se realiza con `fetch()` y actualiza la fila sin recargar.
- Se añadieron estadísticas básicas en cabecera:
  - total de tickets
  - abiertos (`nuevo` + `pendiente`)
  - cerrados

## Requisitos del backend para que el frontend funcione correctamente

### 1. Autenticación y usuario
- `POST /api/v1/auth/login`
  - Request JSON: `username`, `password`
  - Response JSON esperado: `access_token`, `token_type`, `expires_in`
- `GET /api/v1/auth/me`
  - Header: `Authorization: Bearer {token}`
  - Response JSON esperado: `username`, `role`

### 2. Endpoints de ticket del ciudadano
- `POST /api/tickets`
  - Header: `Authorization: Bearer {token}`
  - Request JSON:
    - `titulo`
    - `descripcion`
    - `ubicacion`
    - `categoria_sugerida`
  - Response JSON esperado:
    - `ticket_id`
    - `estado`
    - `fecha_creacion`
- `GET /api/tickets/{ticket_id}`
  - No requiere autenticación según el diseño actual del frontend.
  - Response JSON esperado:
    - `ticket_id`
    - `titulo`
    - `estado`
    - `urgencia`
    - `respuesta_municipal`

### 3. Endpoints de ticket del worker/admin
- `GET /api/worker/tickets`
  - Header: `Authorization: Bearer {token}`
  - Response JSON esperado: lista de tickets
  - Cada ticket debe incluir al menos:
    - `ticket_id`
    - `titulo`
    - `urgencia`
    - `estado`
    - `respuesta_municipal` (o campo equivalente)
- `PUT /api/worker/tickets/{ticket_id}`
  - Header: `Authorization: Bearer {token}`
  - Request JSON:
    - `estado`
    - `respuesta`
  - Response JSON esperado: ticket actualizado o resultado de la operación

### 4. Validación de roles
- El backend debe validar el rol del usuario en cada request protegida.
- Las rutas de trabajo admin deben exigir `admin`.
- Las rutas de ciudadano deben exigir `citizen`.

### 5. Valores esperados
- Estados posibles: `nuevo`, `pendiente`, `cerrado`
- Urgencias posibles: `alta`, `media`, `baja`
- Categorías sugeridas (frontend): `infraestructura`, `limpieza`, `iluminación`, `ruido`, `otros`

### 6. Comportamiento esperado
- Las peticiones desde el frontend deben devolver JSON.
- No deben producir redirecciones HTML en los endpoints de API.
- Si una petición falla, debe devolver una respuesta de error clara para que el frontend pueda mostrarla.

## Nota importante
Actualmente, el backend revisado tiene implementados únicamente:
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/tickets/spec`

Por lo tanto, para que el frontend de tickets funcione completamente es imprescindible implementar los endpoints de tickets listados arriba.
