import RPi.GPIO as GPIO
from grove.adc import ADC
from config import DB_PATH, LIGHT_SENSOR_PIN, SOUND_SENSOR_PIN, MOTION_SENSOR_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)

adc = ADC()

def read_light(): return adc(LIGHT_SENSOR_PIN)
def read_sound(): return adc(SOUND_SENSOR_PIN)
def read_motion(): return GPIO.input(MOTION_SENSOR_PIN)
def read_all(): return {"light":read_light(),"sound":read_sound(),"pir":read_motion()}
def cleanup(): GPIO.cleanup()

if __name__ == "__main__" :
  import time
  while True :
    print(read_all())
    time.sleep(1)
