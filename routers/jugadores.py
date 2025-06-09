from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models_sqlmodel import Jugador  # Asegúrate de tener Jugador importado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/jugadores", response_class=HTMLResponse)
async def mostrar_jugadores(request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Jugador).where(Jugador.is_active == True))
    jugadores = result.all()
    return templates.TemplateResponse("Jugadores/list.html", {
        "request": request,
        "jugadores": jugadores
    })
