import asyncio
import uvicorn
import sqlite3
from config import DB_PATH,API_PORT
from web.api import app
from capteurs import read_all, cleanup
from led import allumer_led, eteindre_led, changer_luminosite

async def boucle_led():
  while True :
    
    await asyncio.sleep(0.1)

async def main():
  asyncio.create_task(boucle_led())
  config = uvicorn.Config(app=app, host="0.0.0.0", port=API_PORT)
  server = uvicorn.Server(config)
  await server.serve()

if __name__ == "__main__":
  asyncio.run(main())
