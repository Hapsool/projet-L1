import board
import neopixel
from config import DB_PATH, NUM_LEDS

LED_PIN = board.D18
STATE = False

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=0.3,
    auto_write=False,
    pixel_order=neopixel.GRB
)

def eteindre_led():
    """Colore toutes les leds en noir"""
    global STATE
    STATE = False
    pixels.fill((0, 0, 0))
    pixels.show()

def allumer_led(couleurs):
    """Peut être utiliser aussi pour rechanger la couleur"""
    global STATE
    STATE = True
    if len(couleurs) == 3 :
        pixels.fill(couleurs)
    else :
        for i in range(NUM_LEDS):
            pixels[i] = couleurs[i]
    pixels.show()

def toggle_led(couleurs):
    global STATE
    if STATE == True :
        eteindre_led()
    else :
        allumer_led(couleurs)


def changer_luminosite(valeur:int):
    """valeur : entre 0 et 100"""
    pixels.brightness = valeur/100

if __name__ == "__main__":
    import time
    c = [(255,255,255) for i in range(64)]
    time.sleep(1)
    allumer_led(c)
    time.sleep(3)
    eteindre_led()
