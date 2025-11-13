import sqlite3
from config import DB_PATH

def setup():
  connect = sqlite3.connect(DB_PATH)
  connect.execute("PRAGMA journal_mode=WAL;")
  connect.executescript("""
  CREATE TABLE IF NOT EXISTS mesures (
    pir INTEGER,
    light INTEGER,
    sound INTEGER 
  );
  CREATE TABLE IF NOT EXISTS config (
    mode TEXT NOT NULL,
    luminosite INTEGER NOT NULL,
    jeu_de_lumiere TEXT NOT NULL
  );
  CREATE TABLE IF NOT EXISTS couleurs (
    id INTEGER PRIMARY KEY,
    R INTEGER NOT NULL,
    G INTEGER NOT NULL,
    B INTEGER NOT NULL
  );
  CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    date_creation TEXT,
    matrice TEXT NOT NULL
  );
  """)
  connect.commit()
  connect.close()

if __name__ == "__main__":
  setup()
