# app.py — SmartLight Web (Raspberry Pi)
# Modes: MANUEL | AUTO (PIR + Lux) | CLAP (double tape des mains)
# Historique en SQLite, API REST, page web intégrée.

import os, time, math, threading, sqlite3, datetime
from flask import Flask, request, jsonify, render_template
from gpiozero import LED, MotionSensor

# ========= CONFIG =========
# GPIO Grove (à adapter si besoin)
GPIO_RELAY = 16      # D16 → relais / lampe (ON/OFF)
GPIO_PIR   = 5       # D5  → capteur de présence PIR

# ADC (choisir un backend)
USE_MCP3008 = False
USE_ADS1x15 = True   # ← par défaut: Grove I2C ADC (ADS1115/ADS1015)

ADC_CH_SOUND = 0     # canal du micro
ADC_CH_LUX   = 1     # canal luminosité (LDR) si utilisé

# --- Paramètres Auto ---
LUX_SEUIL_DEFAULT = 400       # lux seuil (configurable via API)
AUTO_PERIOD_S = 0.5           # période de décision auto

# --- Paramètres Clap x2 ---
CLAP_RATIO = 3.0              # sensibilité: plus petit = plus sensible
CLAP_MIN_FRAC = 0.06          # seuil mini absolu (fraction de l'échelle ADC)
CLAP_DOUBLE_MIN_MS = 120
CLAP_DOUBLE_MAX_MS = 600
CLAP_COOLDOWN_MS   = 1500
EMA_ALPHA = 0.02              # lissage de l'enveloppe

# DB
DB_PATH = os.path.join("db", "smartlight.db")
os.makedirs("db", exist_ok=True)

# ========= HARDWARE =========
relay = LED(GPIO_RELAY)           # gpiozero LED convient pour piloter un relais ON/OFF
pir   = MotionSensor(GPIO_PIR)

# ADC abstraction
adc_read = None
adc_fullscale = 1.0
using_adc = False

if USE_MCP3008:
    try:
        from gpiozero import MCP3008
        ch_sound = MCP3008(channel=ADC_CH_SOUND)
        ch_lux   = MCP3008(channel=ADC_CH_LUX)
        using_adc = True
        adc_fullscale = 1.0  # gpiozero renvoie 0..1
        def adc_read(channel):
            return (ch_sound.value if channel==ADC_CH_SOUND else ch_lux.value)
    except Exception as e:
        print("[WARN] MCP3008 non initialisé:", e)

if USE_ADS1x15 and not using_adc:
    try:
        import board, busio
        import adafruit_ads1x15.ads1115 as ADS
        from adafruit_ads1x15.analog_in import AnalogIn
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        ch_sound = AnalogIn(ads, getattr(ADS, f"P{ADC_CH_SOUND}"))
        ch_lux   = AnalogIn(ads, getattr(ADS, f"P{ADC_CH_LUX}"))
        using_adc = True
        adc_fullscale = 3.3   # approx tension max lue
        def adc_read(channel):
            return (ch_sound.voltage if channel==ADC_CH_SOUND else ch_lux.voltage)
    except Exception as e:
        print("[WARN] ADS1x15 non initialisé:", e)

# ========= ETAT GLOBAL =========
STATE = {
    "mode": "MANUEL",      # MANUEL | AUTO | CLAP
    "led": False,          # lampe ON/OFF
    "intensity": 1.0,      # 1.0 si relais (ON=1, OFF=0), slider possible si LED PWM/NeoPixel
    "presence": False,
    "lux": 0.0,
    "seuil": LUX_SEUIL_DEFAULT,
    "supportsIntensity": False  # True si tu montes une LED 5V avec PWM/NeoPixel
}
state_lock = threading.Lock()

# ========= DB =========
def db_init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS actions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        led_state TEXT,     -- 'ON'/'OFF'
        lux REAL,
        presence INTEGER,
        mode TEXT,
        reason TEXT,
        intensity REAL
    )""")
    conn.commit(); conn.close()

def log_action(led_state, lux, presence, mode, reason, intensity):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO actions VALUES(NULL,?,?,?,?,?,?,?)",
              (datetime.datetime.now().isoformat(timespec="seconds"),
               led_state, float(lux), int(bool(presence)), mode, reason, float(intensity)))
    conn.commit(); conn.close()

def set_led(on: bool, reason=""):
    with state_lock:
        STATE["led"] = bool(on)
        # Intensité: si relais, 1.0 quand ON, 0.0 quand OFF
        STATE["intensity"] = 1.0 if on else 0.0
        led_state = "ON" if on else "OFF"
        lux = STATE["lux"]; presence = STATE["presence"]; mode = STATE["mode"]
        # Action physique
        relay.on() if on else relay.off()
    log_action(led_state, lux, presence, mode, reason, STATE["intensity"])

# ========= THREADS =========
def sensors_loop():
    """
    Lit présence PIR et lux (si capteur branché) ~10 Hz.
    Si pas de capteur lux dispo, garde la dernière valeur.
    """
    while True:
        presence = pir.motion_detected
        lux_val = None
        if using_adc:
            try:
                raw = adc_read(ADC_CH_LUX)
                # approx: map voltage->lux (à calibrer). Si MCP3008 (0..1), multiplie par 1000.
                if USE_MCP3008:
                    lux_val = float(raw) * 1000.0
                else:
                    lux_val = float(raw) * (1000.0 / adc_fullscale)
            except Exception:
                pass
        with state_lock:
            STATE["presence"] = presence
            if lux_val is not None:
                STATE["lux"] = round(lux_val, 1)
        time.sleep(0.1)

def auto_loop():
    """
    Applique la règle AUTO toutes les AUTO_PERIOD_S.
    """
    while True:
        time.sleep(AUTO_PERIOD_S)
        with state_lock:
            if STATE["mode"] != "AUTO":
                continue
            presence = STATE["presence"]
            lux = STATE["lux"]
            seuil = STATE["seuil"]
            led_now = STATE["led"]
        # Règle simple + anti-flash implicite (ne toggle que si changement)
        if presence and lux < seuil:
            if not led_now:
                set_led(True, reason="AUTO.rule")
        else:
            if led_now:
                set_led(False, reason="AUTO.rule")

def clap_loop():
    """
    Détecte un double clap (deux pics sonores dans une fenêtre temporelle).
    Requiert un micro analogique sur ADC_CH_SOUND.
    """
    if not using_adc:
        print("[INFO] Clap: ADC non dispo → thread inactif.")
        while True:
            time.sleep(1)
    baseline = 0.0
    last_peak_ts = None
    cooldown_until = 0

    def read_amp_norm():
        try:
            v = adc_read(ADC_CH_SOUND)   # tension (ADS) ou 0..1 (MCP)
            x = float(v) / (adc_fullscale if not USE_MCP3008 else 1.0)
            return max(0.0, min(1.0, x))
        except Exception:
            return 0.0

    while True:
        time.sleep(0.01)  # ~100 Hz
        with state_lock:
            if STATE["mode"] != "CLAP":
                continue
            led_now = STATE["led"]

        x = read_amp_norm()
        baseline = (1-EMA_ALPHA)*baseline + EMA_ALPHA*x

        now = int(time.time()*1000)
        if now < cooldown_until:
            continue

        threshold = max(CLAP_MIN_FRAC, baseline * CLAP_RATIO)
        is_peak = x > threshold

        if is_peak:
            if last_peak_ts is None:
                last_peak_ts = now
            else:
                dt = now - last_peak_ts
                last_peak_ts = now
                if CLAP_DOUBLE_MIN_MS <= dt <= CLAP_DOUBLE_MAX_MS:
                    set_led(not led_now, reason=f"CLAP.dt={dt}ms")
                    cooldown_until = now + CLAP_COOLDOWN_MS

# ========= FLASK =========
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state")
def api_state():
    with state_lock:
        return jsonify(STATE)

@app.route("/api/on", methods=["POST"])
def api_on():
    with state_lock:
        STATE["mode"] = "MANUEL"
    set_led(True, reason="MANUEL")
    return jsonify(ok=True)

@app.route("/api/off", methods=["POST"])
def api_off():
    with state_lock:
        STATE["mode"] = "MANUEL"
    set_led(False, reason="MANUEL")
    return jsonify(ok=True)

@app.route("/api/mode", methods=["POST"])
def api_mode():
    data = request.get_json(force=True, silent=True) or {}
    mode = str(data.get("mode", "MANUEL")).upper()
    if mode not in ("MANUEL","AUTO","CLAP"):
        return jsonify(ok=False, error="mode invalide"), 400
    with state_lock:
        STATE["mode"] = mode
    return jsonify(ok=True, mode=mode)

@app.route("/api/seuil", methods=["POST"])
def api_seuil():
    data = request.get_json(force=True, silent=True) or {}
    try:
        val = int(data.get("seuil", STATE["seuil"]))
    except Exception:
        return jsonify(ok=False, error="seuil invalide"), 400
    with state_lock:
        STATE["seuil"] = val
    return jsonify(ok=True, seuil=val)

@app.route("/api/history")
def api_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, led_state, lux, presence, mode, reason, intensity FROM actions ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

# ========= MAIN =========
if __name__ == "__main__":
    db_init()
    threading.Thread(target=sensors_loop, daemon=True).start()
    threading.Thread(target=auto_loop, daemon=True).start()
    threading.Thread(target=clap_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
