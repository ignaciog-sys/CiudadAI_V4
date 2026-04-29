from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from httpx import HTTPStatusError, RequestError

from services.api_client import api_client

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


def _authorized_role(request: Request, expected_role: str) -> bool:
    return request.session.get("access_token") and request.session.get("role") == expected_role


@router.get("/")
async def home(request: Request):
    if request.session.get("access_token"):
        role = request.session.get("role")
        if role == "admin":
            return RedirectResponse(url="/admin/dashboard", status_code=303)
        return RedirectResponse(url="/citizen/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)


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
        import httpx

        async with httpx.AsyncClient(base_url=api_client.base_url, timeout=10.0) as client:
            response = await client.get(
                "/api/v1/admin/dashboard",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            admin_data = response.json()
    except (HTTPStatusError, RequestError):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    context = {
        "request": request,
        "current_user": current_user,
        "admin_data": admin_data,
    }
    return templates.TemplateResponse("admin_dashboard.html", context)


@router.get("/admin/tickets")
async def admin_list_tickets(request: Request):
    if not _authorized_role(request, "admin"):
        return JSONResponse({"ok": False, "error": "No autorizado"}, status_code=403)

    token = request.session.get("access_token")
    tickets = await api_client.listar_tickets_worker(token)
    if tickets is None:
        return JSONResponse(
            {"ok": False, "error": "No se pudo obtener la lista de tickets."},
            status_code=502,
        )

    return tickets


@router.put("/admin/tickets/{ticket_id}")
async def admin_update_ticket(ticket_id: str, request: Request):
    if not _authorized_role(request, "admin"):
        return JSONResponse({"ok": False, "error": "No autorizado"}, status_code=403)

    body = await request.json()
    estado = body.get("estado")
    respuesta = body.get("respuesta")
    token = request.session.get("access_token")

    if not estado or respuesta is None:
        return JSONResponse(
            {"ok": False, "error": "Faltan datos de estado o respuesta."},
            status_code=400,
        )

    updated = await api_client.actualizar_ticket(token, ticket_id, estado, respuesta)
    if updated is None:
        return JSONResponse(
            {"ok": False, "error": "No se pudo actualizar el ticket."},
            status_code=502,
        )

    return updated


# ============ RUTAS CIUDADANO ============

@router.get("/citizen/dashboard")
async def citizen_dashboard(request: Request):
    token = request.session.get("access_token")
    role = request.session.get("role")

    if not token or role != "citizen":
        return RedirectResponse(url="/login", status_code=303)

    try:
        current_user = await api_client.me(token)
        import httpx

        async with httpx.AsyncClient(base_url=api_client.base_url, timeout=10.0) as client:
            response = await client.get(
                "/api/v1/citizen/dashboard",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            citizen_data = response.json()
    except (HTTPStatusError, RequestError):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    context = {
        "request": request,
        "current_user": current_user,
        "citizen_data": citizen_data,
    }
    return templates.TemplateResponse("citizen_dashboard.html", context)


@router.post("/citizen/tickets")
async def citizen_create_ticket(
    request: Request,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    ubicacion: str = Form(...),
    categoria_sugerida: str = Form(...),
):
    if not _authorized_role(request, "citizen"):
        return JSONResponse({"ok": False, "error": "No autorizado"}, status_code=403)

    token = request.session.get("access_token")
    created = await api_client.crear_ticket(token, titulo, descripcion, ubicacion, categoria_sugerida)
    if created is None:
        return JSONResponse({"ok": False, "error": "No se pudo crear el ticket."}, status_code=502)

    ticket_id = created.get("ticket_id") or created.get("id")
    return {"ok": True, "ticket_id": ticket_id}


@router.get("/citizen/tickets/{ticket_id}")
async def citizen_get_ticket(ticket_id: str, request: Request):
    if not _authorized_role(request, "citizen"):
        return JSONResponse({"ok": False, "error": "No autorizado"}, status_code=403)

    ticket = await api_client.obtener_ticket(ticket_id)
    if ticket is None:
        return JSONResponse({"ok": False, "error": "Ticket no encontrado."}, status_code=404)

    return ticket
