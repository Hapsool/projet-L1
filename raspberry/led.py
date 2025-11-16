import board
import neopixel
import sqlite3
from config import DB_PATH, NUM_LEDS

LED_PIN = board.D18

conn = sqlite3.connect(DB_PATH)
luminosite = conn.execute("SELECT luminosite FROM config").fetchone()[0]
conn.close()

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=luminosite/100,
    auto_write=False,
    pixel_order=neopixel.GRB
)

def eteindre_led():
    pixels.fill((0, 0, 0))
    pixels.show()

def allumer_led():
    conn = sqlite3.connect(DB_PATH)
    couleurs = conn.execute("SELECT r, g, b FROM couleurs ORDER BY id").fetchall() # ex : [(255,255,255),(...),...]
    conn.close()
    for i in range(NUM_LEDS):
        pixels[i] = couleurs[i]
    pixels.show()
