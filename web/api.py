import uvicorn
import sqlite3
from config import DB_PATH
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.post("/led/state")
async def update_led_state(request: Request):
    data = await request.form()
    etat = int(data.get("etat"))

    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE config SET etat = ?", (etat,))
    conn.commit()
    conn.close()

    return {"etat": etat}

@app.post("/led/luminosity")
async def update_led_luminosity(request: Request):
    data = await request.form()
    luminosite = float(data.get("luminosite"))

    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE config SET luminosite = ?", (luminosite,))
    conn.commit()
    conn.close()

    return {"luminosite": luminosite}

# -------page d'accueil------
@app.get("/")

def start(request:Request) -> str:
    return templates.TemplateResponse('accueil',{'request': request,'title':'Lampe Intelligente'})
#--------------fin---------------

if __name__ == "__main__":
  from config import API_PORT
  uvicorn.run(app, host="0.0.0.0", port=API_PORT)
