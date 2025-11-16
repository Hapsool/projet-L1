import board
import neopixel
import sqlite3
from config import DB_PATH

LED_PIN = board.D18
NUM_LEDS = 64

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=0.3,
    auto_write=False,
    pixel_order=neopixel.GRB
)


def eteindre_led():
  pass
