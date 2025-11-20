import board
import neopixel
from config import DB_PATH, NUM_LEDS

LED_PIN = board.D18

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=0.3,
    auto_write=False,
    pixel_order=neopixel.GRB
)

def eteindre_led():
    """Colore toutes les leds en noir"""
    pixels.fill((0, 0, 0))
    pixels.show()

def allumer_led(couleurs:list[tuple[int,int,int]]):
    """Peut être utiliser aussi pour rechanger la couleur"""
    for i in range(NUM_LEDS):
        pixels[i] = couleurs[i]
    pixels.show()

def changer_luminosite(valeur:int):
    """valeur : entre 0 et 100"""
    pixels.brightness = valeur/100

if __main__ == "__main__":
    import time
    c = [(255,255,255) for i in range(64)]
    time.sleep(1)
    allumer_led(c)
    time.sleep(3)
    eteindre_led()
