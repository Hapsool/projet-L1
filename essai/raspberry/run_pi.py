import time, sqlite3
from config import DB_PATH, NUM_LEDS
from capteurs import read_all, cleanup
from led import allumer_led, eteindre_led, changer_luminosite
INTERVALLE=0.5
def get_config():
    with sqlite3.connect(DB_PATH) as c:
        r=c.execute("SELECT mode,luminosite,jeu_de_lumiere,etat FROM config LIMIT 1").fetchone()
    return {"mode":r[0],"luminosite":r[1],"jeu_de_lumiere":r[2],"etat":r[3]}
def update_mesures(m):
    with sqlite3.connect(DB_PATH) as c:
        c.execute("UPDATE mesures SET pir=?,light=?,sound=?", (m["pir"],m["light"],m["sound"]))
        c.commit()
def appliquer_config(cfg,m):
    if cfg["etat"]==0: eteindre_led(); return
    changer_luminosite(cfg["luminosite"])
    if cfg["mode"]=="manual":
        allumer_led([(255,255,255)]*NUM_LEDS)
    elif cfg["mode"]=="presence":
        allumer_led([(0,150,255)]*NUM_LEDS) if m["pir"] else eteindre_led()
    elif cfg["mode"]=="auto":
        if m["light"]==0 and m["pir"]: allumer_led([(255,255,255)]*NUM_LEDS)
        else: eteindre_led()
def main():
    try:
        while True:
            m=read_all()
            update_mesures(m)
            cfg=get_config()
            appliquer_config(cfg,m)
            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        eteindre_led(); cleanup()
if __name__=="__main__": main()
