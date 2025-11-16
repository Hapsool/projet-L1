import board
import neopixel
from config import DB_PATH

LED_PIN = board.D18
NUM_LEDS = 64

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=0.3,      # intensité globale (0.0 à 1.0)
    auto_write=False,     # écriture automatique
    pixel_order=neopixel.GRB  # l'ordre le plus courant
)


def eteindre_led():
  pass
