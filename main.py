from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers import jugadores, player_web

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(jugadores.router)
app.include_router(player_web.router)

@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/planeacion", response_class=HTMLResponse)
async def mostrar_planeacion(request: Request):
    return templates.TemplateResponse("planeacion.html", {"request": request})

@app.get("/diseno", response_class=HTMLResponse)
async def mostrar_diseno(request: Request):
    return templates.TemplateResponse("diseño.html", {"request": request})

@app.get("/desarrollo", response_class=HTMLResponse)
async def mostrar_fase_desarrollo(request: Request):
    return templates.TemplateResponse("desarrollo.html", {"request": request})

@app.get("/desarrollador", response_class=HTMLResponse)
async def mostrar_desarrollador(request: Request):
    return templates.TemplateResponse("desarrollador.html", {"request": request})
