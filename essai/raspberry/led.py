import time, board, neopixel
from config import NUM_LEDS
LED_PIN = board.D18
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.3, auto_write=False, pixel_order=neopixel.GRB)
def eteindre_led(): pixels.fill((0,0,0)); pixels.show()
def allumer_led(c): 
    for i in range(NUM_LEDS): pixels[i]=c[i] if i<len(c) else (0,0,0)
    pixels.show()
def changer_luminosite(v): pixels.brightness=max(0,min(100,v))/100; pixels.show()
