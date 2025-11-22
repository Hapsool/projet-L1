# config.py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "data_base.db"
API_PORT = 8000
NUM_LEDS = 64
LIGHT_SENSOR_PIN = 17
SOUND_SENSOR_PIN = 5
MOTION_SENSOR_PIN = 16
MODES = ["auto", "manual", "presence"]
DEFAULT_MODE = "manual"
