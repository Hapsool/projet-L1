# setup_database.py
import sqlite3
from config import DB_PATH, NUM_LEDS
def setup():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS mesures (
            pir INTEGER,
            light INTEGER,
            sound INTEGER
        );
        CREATE TABLE IF NOT EXISTS config (
            mode TEXT NOT NULL,
            luminosite INTEGER NOT NULL,
            jeu_de_lumiere TEXT NOT NULL,
            etat INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS couleurs (
            id INTEGER PRIMARY KEY,
            r INTEGER NOT NULL,
            g INTEGER NOT NULL,
            b INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            date_creation TEXT,
            matrice TEXT NOT NULL
        );
    """)
    if conn.execute("SELECT COUNT(*) FROM mesures").fetchone()[0] == 0:
        conn.execute("INSERT INTO mesures VALUES (0,0,0)")
    if conn.execute("SELECT COUNT(*) FROM config").fetchone()[0] == 0:
        conn.execute("INSERT INTO config VALUES ('manual',30,'static',0)")
    if conn.execute("SELECT COUNT(*) FROM couleurs").fetchone()[0] == 0:
        conn.executemany("INSERT INTO couleurs VALUES (?,?,?,?)",
                         [(i,255,255,255) for i in range(1,NUM_LEDS+1)])
    conn.commit()
    conn.close()
if __name__ == "__main__":
    setup()
