import RPi.GPIO as GPIO
from config import LIGHT_SENSOR_PIN, SOUND_SENSOR_PIN, MOTION_SENSOR_PIN
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)
GPIO.setup(MOTION_SENSOR_PIN, GPIO.IN)
def read_light(): return GPIO.input(LIGHT_SENSOR_PIN)
def read_sound(): return GPIO.input(SOUND_SENSOR_PIN)
def read_motion(): return GPIO.input(MOTION_SENSOR_PIN)
def read_all(): return {"light":read_light(),"sound":read_sound(),"pir":read_motion()}
def cleanup(): GPIO.cleanup()
