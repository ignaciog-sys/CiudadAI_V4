from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from httpx import HTTPStatusError, RequestError

from services.api_client import api_client

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


def _format_datetime(value: str | datetime | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return str(value)
    return dt.strftime("%d/%m/%Y %H:%M")


@router.get("/")
async def home(request: Request, ticket_id: int | None = None):
    if request.session.get("access_token"):
        # Redirigir según rol
        role = request.session.get("role")
        if role == "admin":
            return RedirectResponse(url="/admin/dashboard", status_code=303)
        else:
            return RedirectResponse(url="/citizen/dashboard", status_code=303)

    search_result = None
    search_error = None

    if ticket_id is not None:
        try:
            import httpx
            async with httpx.AsyncClient(base_url=api_client.base_url, timeout=10.0) as client:
                response = await client.get(f"/api/v1/citizen/tickets/{ticket_id}/status")
                response.raise_for_status()
                search_result = response.json()
                if search_result and search_result.get("fecha_creacion"):
                    search_result["fecha_creacion"] = _format_datetime(search_result["fecha_creacion"])
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                search_error = "No se ha encontrado ninguna incidencia con ese ID."
            else:
                search_error = "Error al consultar la incidencia."
        except RequestError:
            search_error = "No se pudo conectar con el backend."

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "ticket_id": ticket_id,
            "search_result": search_result,
            "search_error": search_error,
            "form_error": None,
        },
    )


@router.get("/dashboard")
async def dashboard(request: Request):
    token = request.session.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)

    try:
        current_user = await api_client.me(token)
        items = await api_client.items(token)
    except (HTTPStatusError, RequestError):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    context = {
        "request": request,
        "current_user": current_user,
        "items": items.items,
    }
    return templates.TemplateResponse("dashboard.html", context)


# ============ RUTAS ADMIN ============

@router.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    token = request.session.get("access_token")
    role = request.session.get("role")
    
    if not token or role != "admin":
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        current_user = await api_client.me(token)
        # Llamar al endpoint de admin
        import httpx
        async with httpx.AsyncClient(base_url=api_client.base_url, timeout=10.0) as client:
            dashboard_response = await client.get(
                "/api/v1/admin/dashboard",
                headers={"Authorization": f"Bearer {token}"},
            )
            dashboard_response.raise_for_status()
            admin_data = dashboard_response.json()

            stats_response = await client.get(
                "/api/v1/admin/stats",
                headers={"Authorization": f"Bearer {token}"},
            )
            stats_response.raise_for_status()
            admin_stats = stats_response.json()

            tickets_response = await client.get(
                "/api/v1/admin/tickets",
                headers={"Authorization": f"Bearer {token}"},
                params={"limit": 10},
            )
            tickets_response.raise_for_status()
            admin_tickets = tickets_response.json()
            for ticket in admin_tickets:
                if ticket and ticket.get("fecha"):
                    ticket["fecha"] = _format_datetime(ticket["fecha"])
    except (HTTPStatusError, RequestError):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)
    
    context = {
        "request": request,
        "current_user": current_user,
        "admin_data": admin_data,
        "admin_stats": admin_stats,
        "admin_tickets": admin_tickets,
    }
    return templates.TemplateResponse("admin_dashboard.html", context)


@router.get("/citizen/report")
async def citizen_report_form(request: Request):
    return RedirectResponse(url="/", status_code=303)


@router.post("/citizen/report")
async def citizen_report_submit(
    request: Request,
    nombre: str = Form(...),
    apellidos: str = Form(...),
    nif: str = Form(...),
    telefono: str = Form(""),
    phone_prefix: str = Form("+34"),
    phone_local: str = Form(""),
    email: str = Form(...),
    categoria: str = Form(...),
    description: str = Form(...),
    direccion_persona: str = Form(...),
    ubicacion_incidencia: str = Form(...),
):
    if phone_prefix and phone_local:
        telefono = f"{phone_prefix.strip()} {phone_local.strip()}"

    payload = {
        "nombre": nombre,
        "apellidos": apellidos,
        "nif": nif,
        "telefono": telefono,
        "email": email,
        "categoria": categoria,
        "description": description,
        "direccion_persona": direccion_persona,
        "ubicacion_incidencia": ubicacion_incidencia,
    }
    try:
        ticket = await api_client.create_ticket(payload)
    except HTTPStatusError as exc:
        error_detail = "No se pudo enviar el reporte. Inténtalo de nuevo más tarde."
        try:
            body = exc.response.json()
            if isinstance(body, dict):
                detail = body.get("detail") or body.get("message")
                if detail:
                    error_detail = f"No se pudo enviar el reporte: {detail}"
        except ValueError:
            pass
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "ticket_id": None,
                "search_result": None,
                "search_error": None,
                "form_error": error_detail,
            },
            status_code=exc.response.status_code if exc.response is not None else 503,
        )
    except RequestError:
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "ticket_id": None,
                "search_result": None,
                "search_error": None,
                "form_error": "No se pudo conectar con el backend.",
            },
            status_code=503,
        )

    return templates.TemplateResponse(
        "ticket_success.html",
        {"request": request, "ticket": ticket},
    )


# ============ RUTAS CIUDADANO ============

@router.get("/citizen/dashboard")
async def citizen_dashboard(request: Request):
    token = request.session.get("access_token")
    current_user = None
    if token:
        try:
            current_user = await api_client.me(token)
        except (HTTPStatusError, RequestError):
            request.session.clear()
            current_user = None

    try:
        import httpx
        async with httpx.AsyncClient(base_url=api_client.base_url, timeout=10.0) as client:
            response = await client.get("/api/v1/citizen/dashboard")
            response.raise_for_status()
            citizen_data = response.json()
    except (HTTPStatusError, RequestError):
        return templates.TemplateResponse(
            "citizen_dashboard.html",
            {"request": request, "current_user": current_user, "citizen_data": None, "error": "No se pudo cargar la información del ciudadano."},
            status_code=503,
        )

    context = {
        "request": request,
        "current_user": current_user,
        "citizen_data": citizen_data,
    }
    return templates.TemplateResponse("citizen_dashboard.html", context)
