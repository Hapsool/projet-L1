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

@app.post("/controle")
async def controle_led(request: Request):
  data =  await request.form()
  luminosite = float(data.get("luminosite"))
  etat = int(data.get("etat"))
  
  conn = sqlite3.connect(DB_PATH)
  conn.execute("UPDATE config SET luminosite = ?",(luminosite,))
  conn.execute("UPDATE config SET etat = ?",(etat,))
  conn.commit()
  conn.close()
  
  return {"luminosite":luminosite,"etat":etat}


if __name__ == "__main__":
  from config import PORT
  uvicorn.run(app, host="0.0.0.0", port=PORT)
