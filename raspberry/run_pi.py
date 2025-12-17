import asyncio
import uvicorn
import sqlite3
from config import DB_PATH,API_PORT,NUM_LEDS
from web.api import app
from raspberry.capteurs import read_light, read_sound, read_motion, read_all, cleanup
from raspberry.led import allumer_led, eteindre_led, changer_luminosite, toggle_led

animation_task = None

last_state = {
  "etat":None,
  "luminosite":None,
  "jeu":None,
  "animation":None,
  "couleur":None,
  "image":None
}

async def boucle_capteurs():
  """Mise à jour les valeurs des capteurs dans la base de donnée toutes les 0.5 secondes."""
  while True:
    sensor = read_all()
    conn = sqlite3.connect(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE mesures SET pir = ?,light = ?, sound = ?", (sensor["pir"],sensor["light"],sensor["sound"]))
    conn.commit()
    conn.close()
    await asyncio.sleep(0.5)

async def strobe():
  """Animation Strobe"""
  try :
    while True:
      allumer_led((255,0,0))
      for i in range(1,256):
        allumer_led((255-i,i,0))
        await asyncio.sleep(0.035)
      allumer_led((0,255,0))
      for i in range(1,256):
        allumer_led((0,255-i,i))
        await asyncio.sleep(0.035)
      allumer_led((0,0,255))
      for i in range(1,256):
        allumer_led((i,0,255-i))
        await asyncio.sleep(0.035)
  except asyncio.CancelledError :
    eteindre_led()
    raise

async def fade():
  """Animation Fade"""
  try :
    while True:
      allumer_led((255,0,0))
      await asyncio.sleep(1)
      for i in range(1,256) :
        allumer_led((255,i,i))
        await asyncio.sleep(0.005)
      allumer_led((0,255,0))
      await asyncio.sleep(1)
      for i in range(1,256) :
        allumer_led((i,255,i))
        await asyncio.sleep(0.005)
      allumer_led((0,0,255))
      await asyncio.sleep(1)
      for i in range(1,256) :
        allumer_led((i,i,255))
        await asyncio.sleep(0.005)
  except asyncio.CancelledError :
    eteindre_led()
    raise


async def flash():
  """Animation Flash"""
  try :
    while True:
      allumer_led((255,0,0))
      await asyncio.sleep(1.5)
      allumer_led((0,255,0))
      await asyncio.sleep(1.5)
      allumer_led((0,0,255))
      await asyncio.sleep(1.5)
  except asyncio.CancelledError :
    eteindre_led()
    raise

def wheel(pos):
  """Pour l'animation Rainbow"""
  if pos < 85:
      return (pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
      pos -= 85
      return (255 - pos * 3, 0, pos * 3)
  else:
      pos -= 170
      return (0, pos * 3, 255 - pos * 3)

async def rainbow():
  """Animation Rainbow"""
  try :
    while True:
        for j in range(255):
          l = []
          for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            l.append(wheel(rc_index & 255))
          allumer_led(l)
          await asyncio.sleep(0.01)
  except asyncio.CancelledError :
    eteindre_led()
    raise

def stop_animation():
  """Stop l'animation joué"""
  global animation_task
  if animation_task is not None and not animation_task.done():
    animation_task.cancel()
    animation_task = None
    
def start_animation(anim:str):
  """Commence une nouvelle animation anim"""
  global animation_task
  stop_animation()
  animation_task = asyncio.create_task(anim)
  
def choix_lumiere(etat,luminosite,jeu_de_lumiere,couleur_actif,image_actif,animation_actif) : 
  """Décide de l'état et du jeu de lumière de la led selon ses paramètres."""
  global animation_task,last_state
  
  current_state = {
    "etat":etat,
    "luminosite":luminosite,
    "jeu":jeu_de_lumiere,
    "animation":animation_actif,
    "couleur":couleur_actif,
    "image":image_actif
  }

  if etat == 0 :
    eteindre_led()
  else :
    changer_luminosite(luminosite)
    if jeu_de_lumiere == "animation":
      if (animation_actif != last_state["animation"]) or (jeu_de_lumiere != last_state["jeu"]):
        if animation_actif == "strobe":
          start_animation(strobe())
        elif animation_actif == "fade":
          start_animation(fade())
        elif animation_actif == "flash":
          start_animation(flash())
        elif animation_actif == "rainbow":
          start_animation(rainbow())
        else:
          stop_animation()
    else :
      stop_animation()
      if jeu_de_lumiere == "couleur":
          allumer_led(couleur_actif)
      elif jeu_de_lumiere == "image":
          allumer_led(image_actif)
    last_state = current_state

async def boucle_led():
  """Boucle principale des leds."""
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
    image_actif	= eval(conn.execute("SELECT matrice FROM images WHERE id = ?",(config[7],)).fetchone()[0])
    animation_actif = config[8]
    conn.close()
    if mode == "manual" :
      choix_lumiere(etat,luminosite,jeu_de_lumiere,couleur_actif,image_actif,animation_actif)
    elif mode == "auto" :
      etat_led = 0 if read_light() >= lum_min else read_motion()
      choix_lumiere(etat_led,luminosite,jeu_de_lumiere,couleur_actif,image_actif,animation_actif)
      conn = sqlite3.connect(DB_PATH)
      conn.execute("UPDATE config SET etat = ?",(etat_led,))
      conn.commit()
      conn.close()
    elif mode == "sound":
      etat_led = 1-etat if read_sound() >= audio_min else etat
      choix_lumiere(etat_led,luminosite,jeu_de_lumiere,couleur_actif,image_actif,animation_actif)
      conn = sqlite3.connect(DB_PATH)
      conn.execute("UPDATE config SET etat = ?",(etat_led,))
      conn.commit()
      conn.close()
    await asyncio.sleep(0.1)

@app.on_event("startup")
async def start_background_tasks():
  """Active les boucles principales après le démarrage du site web."""
  asyncio.create_task(boucle_led())
  asyncio.create_task(boucle_capteurs())

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=API_PORT)
