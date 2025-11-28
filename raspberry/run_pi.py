import asyncio
import uvicorn
import sqlite3
from config import DB_PATH,API_PORT
from web.api import app
from capteurs import read_all, cleanup
from led import allumer_led, eteindre_led, changer_luminosite
from capteurs import read_light, read_sound, read_motion, read_all, cleanup

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

async def boucle_led():

  global animation_task

  while True :
    conn = sqlite3.connect(DB_PATH)
    config = conn.execute("SELECT * FROM config")

    mode = config[0]
    etat = config[1]
    luminosite = config[2]
    jeu_de_lumiere = config[3]
    lum_min = config[4]
    audio_min = config[5]
    couleur_actif	= eval(config[6])
    image_actif	= eval(config[7])
    animation_actif = config[8]

    conn.close()

    changer_luminosite(luminosite)

    if mode == "manual" :
      if etat == 0 :
        eteindre_led()
      elif etat == 1 :
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
    elif mode == "auto" :
      pass
    elif mode == "sound":
      pass
    await asyncio.sleep(0.1)

async def main():
  asyncio.create_task(boucle_led())
  asyncio.create_task(boucle_capteurs())
  config = uvicorn.Config(app=app, host="0.0.0.0", port=API_PORT)
  server = uvicorn.Server(config)
  await server.serve()

if __name__ == "__main__":
  asyncio.run(main())
