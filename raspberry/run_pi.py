import asyncio
import uvicorn
import sqlite3
from config import DB_PATH,API_PORT
from web.api import app
from raspberry.capteurs import read_light, read_sound, read_motion, read_all, cleanup
from raspberry.led import allumer_led, eteindre_led, changer_luminosite, toggle_led

animation_task = None

async def boucle_capteurs():
    while True:
      sensor = read_all()
      conn = sqlite3.connect(DB_PATH)
      conn = sqlite3.connect(DB_PATH)
      conn.execute("UPDATE mesures SET pir = ?,light = ?, sound = ?", (sensor["pir"],sensor["light"],sensor["sound"]))
      conn.commit()
      conn.close()
      await asyncio.sleep(0.5)

async def strobe():
  pass

async def fade():
  pass

async def flash():
  pass

async def choix_lumiere(jeu_de_lumiere,couleur_actif,image_actif,animation_actif) : 
  if jeu_de_lumiere == "couleur":
          allumer_led(couleur_actif)
        elif jeu_de_lumiere == "image":
          allumer_led(image_actif)
        elif jeu_de_lumiere == "animation":
            if animation_actif == "strobe":
              if animation_task is None or animation_task.done():
                animation_task = asyncio.create_task(strobe())
            elif animation_actif == "fade":
              if animation_task is None or animation_task.done():
                animation_task = asyncio.create_task(fade())
            else:
              if animation_task is not None and not animation_task.done():
                animation_task.cancel()
                animation_task = None

async def boucle_led():

  global animation_task

  while True :
    conn = sqlite3.connect(DB_PATH)
    config = conn.execute("SELECT * FROM config").fetchone()

    mode = config[0]
    etat = config[1]
    luminosite = config[2]
    jeu_de_lumiere = config[3]
    lum_min = config[4]
    audio_min = config[5]
    couleur_actif	= eval(config[6])
    image_actif	= config[7]
    animation_actif = config[8]

    conn.close()

    changer_luminosite(luminosite)

    if mode == "manual" :
      if etat == 0 :
        eteindre_led()
      elif etat == 1 :
        choix_lumiere(jeu_de_lumiere,couleur_actif,image_actif,animation_actif)

    elif mode == "auto" :
      if read_motion() == 0 :
        eteindre_led()
      elif read_motion() == 1 :
        if read_light() < lum_min :
          choix_lumiere(jeu_de_lumiere,couleur_actif,image_actif,animation_actif)
      conn = sqlite3.connect(DB_PATH)
      conn.execute("UPDATE config SET etat = ?",(read_motion(),))
      conn.commit()
      conn.close()

    elif mode == "sound":
      if read_sound() >= audio_min :
        if etat == 0 :
          choix_lumiere(jeu_de_lumiere,couleur_actif,image_actif,animation_actif)
        elif etat == 1 :
          eteindre_led()
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE config SET etat = ?",((1-etat),))
        conn.commit()
        conn.close()
  
    await asyncio.sleep(0.1)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(boucle_led())
    asyncio.create_task(boucle_capteurs())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
