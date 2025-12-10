import sys
import os
# Ajouter le dossier parent au path pour que Python trouve config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INTENSITE_LUMIERE_DEFAUT
from config import CAPTEUR_LUMIERE_SEUIL_DEFAUT
from config import CAPTEUR_AUDIO_SEUIL_DEFAUT
from config import DB_PATH
#chemin bidouillé qui fonction :
# Chemin absolu vers la base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # dossier où est main.py
DB_FULL_PATH = os.path.join(BASE_DIR, "..", DB_PATH)  # remonte d’un dossier si besoin
print(DB_FULL_PATH)  # pour vérifier

import uvicorn
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI() # Création de l application
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")




#test
@app.get("/test")
async def test():
    return {"message": "Serveur OK"}

#-----------------fonctions get/post------------------
#recup la lumiere ambiante capté
@app.get('/capteur/lumiere')
async def get_led_mode(request: Request):
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()
    cursor. execute("SELECT light FROM mesures LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return {"luminosite": row[0] if row else 0}


#change le mode
@app.post("/led/mode")
async def update_led_mode(request: Request):
    data = await request.form()
    mode = data.get("mode")

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET mode = ?", (mode,))
    conn.commit()
    conn.close()

    return {"mode": mode}

#recup le mode
@app.get('/led/mode')
async def get_led_mode(request: Request):
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()
    cursor. execute("SELECT mode FROM config LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return {"mode": row[0] if row else 0}

#recup les valeurs par defaut seuil audio/lumi et intensité
@app.get('/valeurs_par_defaut')
def get_valeurs_par_defaut():
    return {"audio_min": CAPTEUR_AUDIO_SEUIL_DEFAUT,"lum_min": CAPTEUR_LUMIERE_SEUIL_DEFAUT, "luminosite": INTENSITE_LUMIERE_DEFAUT}

#change seuil luminosite capteur
@app.post("/capteur/seuil_audio")
async def update_type_d_affichage(request: Request):
    audio_min = (await request.body()).decode("utf-8")

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET audio_min = ?", (audio_min,)) 
    conn.commit()
    conn.close()

    return {"audio_min": audio_min}

#recup le seuil audio capteur
@app.get("/capteur/seuil_audio")
def get_audio_min():
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT audio_min FROM config"
    )
    row = cursor.fetchone()
    conn.close()

    audio_min = row[0] if row else None

    return {"audio_min": audio_min}

#change seuil luminosite capteur
@app.post("/capteur/seuil_luminosite")
async def update_type_d_affichage(request: Request):
    lum_min = (await request.body()).decode("utf-8")

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET lum_min = ?", (lum_min,)) 
    conn.commit()
    conn.close()

    return {"lum_min": lum_min}

#recup le seuil lumi capteur
@app.get("/capteur/seuil_luminosite")
def get_lum_min():
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT lum_min FROM config"
    )
    row = cursor.fetchone()
    conn.close()

    lum_min = row[0] if row else None

    return {"lum_min": lum_min}

#change le jeu de lumiere
@app.post("/led/affichage")
async def update_type_d_affichage(request: Request):
    type_affichage = (await request.body()).decode("utf-8")

    MODES_VALIDES = {"couleur", "image", "animation"}

    if type_affichage not in MODES_VALIDES:
        return {"error": "mode invalide"}, 400

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET jeu_de_lumiere = ?", (type_affichage,))
    conn.commit()
    conn.close()

    return {"jeu_de_lumiere": type_affichage}

#donne le jeu de lumiere actuel
@app.get("/led/affichage")
def get_jeu_de_lumiere():
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT jeu_de_lumiere FROM config"
    )
    row = cursor.fetchone()
    conn.close()

    jeu_de_lumiere = row[0] if row else None

    return {"jeu_de_lumiere": jeu_de_lumiere}

#change l'etat ON/OFF
@app.post("/led/state")
async def update_led_state(request: Request):
    data = await request.form()
    etat = int(data.get("etat"))

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET etat = ?", (etat,))
    conn.commit()
    conn.close()

    return {"etat": etat}

@app.get("/led/state")
async def get_led_state(request: Request):
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT etat FROM config LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    return {"etat": row[0] if row else 0}


#change l'intensité de la lumiere des led
@app.post("/led/luminosite")
async def update_led_luminosite(request: Request):
    data = await request.form()
    luminosite = float(data.get("luminosite"))

    conn = sqlite3.connect(DB_FULL_PATH)
    conn.execute("UPDATE config SET luminosite = ?", (luminosite,))
    conn.commit()
    conn.close()

    return {"luminosite": luminosite}

#recup intensite des led

@app.get('/led/luminosite')
async def get_led_luminosite(request: Request):
    conn = sqlite3.connect(DB_FULL_PATH)
    cursor = conn.cursor()
    cursor. execute("SELECT luminosite FROM config LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return {"luminosite": row[0] if row else 0}

# ----------------Chemins des pages -------------------

@app.get("/") # Tt ce qui a apres c lancé quand on est dans le chemin / , qui est donc le root
def home(request:Request) -> str:
    return templates.TemplateResponse('accueil',{'request': request,'title':'Lampe Intelligente'})

@app.get("/information")
def info(request:Request) -> str:
    return templates.TemplateResponse('Information',{'request': request,'title':'Lampe Intelligente'})

@app.get("/personnalisation")
def perso(request:Request) -> str:
    return templates.TemplateResponse('Personnalisation',{'request': request,'title':'Lampe Intelligente'})

@app.get("/parametre")
def perso(request:Request) -> str:
    return templates.TemplateResponse('Parametre',{'request': request,'title':'Lampe Intelligente'})

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug
