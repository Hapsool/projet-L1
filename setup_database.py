import sqlite3
from config import DB_PATH

def setup():
  conn = sqlite3.connect(DB_PATH)
  conn.execute("PRAGMA journal_mode=WAL;")

  # Créations des tables si elles n'existes pas :
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

  # Mise en place des valeurs de départ si les tables sont vides :

  # pour la table mesures :
  resultat = conn.execute("SELECT COUNT(*) FROM mesures")
  nb = resultat.fetchone()[0]
  if nb_mesures == 0 :
    conn.execute("INSERT INTO mesures (pir, light, sound) VALUES (?, ?, ?)", (0,0,0))

  # pour la table config :
  resultat = conn.execute("SELECT COUNT(*) FROM config")
  nb = resultat.fetchone()[0]
  if nb_mesures == 0 :
    conn.execute("INSERT INTO config (mode, luminosite, jeu_de_lumiere) VALUES (?, ?, ?)", ("manual",0,"static"))

  # pour la table couleurs :
  resultat = conn.execute("SELECT COUNT(*) FROM couleurs")
  nb = resultat.fetchone()[0]
  if nb_mesures == 0 :
    conn.executemany("INSERT INTO couleurs (id, r, g, b) VALUES (?, ?, ?, ?)", [(i,0,0,0) for i in range(1,65)])

  # La table images peut être vide.
    
  conn.commit()
  conn.close()

if __name__ == "__main__":
  setup()
