from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from httpx import HTTPStatusError, RequestError

from services.api_client import api_client

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/")
async def home(request: Request):
    if request.session.get("access_token"):
        return RedirectResponse(url="/dashboard", status_code=303)
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
