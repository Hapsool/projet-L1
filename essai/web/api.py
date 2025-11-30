
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent  # dossier /web

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")











import sqlite3
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import DB_PATH, API_PORT
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR/"templates")
def update_config_field(f,v):
    with sqlite3.connect(DB_PATH) as c: c.execute(f"UPDATE config SET {f}=?",(v,)); c.commit()
def fetch_config():
    with sqlite3.connect(DB_PATH) as c:
        r=c.execute("SELECT mode,luminosite,jeu_de_lumiere,etat FROM config LIMIT 1").fetchone()
    return {"mode":r[0],"luminosite":r[1],"jeu_de_lumiere":r[2],"etat":r[3]}
@app.get("/",response_class=HTMLResponse)
async def index(request:Request): return templates.TemplateResponse("index.html",{"request":request,"config":fetch_config()})
@app.post("/led/state")
async def state(etat:int=Form(...)): update_config_field("etat",etat); return {"etat":etat}
@app.post("/led/luminosity")
async def lum(luminosite:int=Form(...)): update_config_field("luminosite",luminosite); return {"luminosite":luminosite}
if __name__=="__main__": uvicorn.run("web.api:app",host="0.0.0.0",port=API_PORT,reload=True)
