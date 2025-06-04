# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers import jugadores, player_web

app = FastAPI()
#app.include_router(jugadores.router)
app.include_router(player_web.router)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

