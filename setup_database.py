import sqlite3
from config import DB_PATH, NUM_LEDS

def setup():
  conn = sqlite3.connect(DB_PATH)
  conn.execute("PRAGMA journal_mode=WAL;")

  # Créations des tables si elles n'existes pas :
  conn.executescript("""
  CREATE TABLE IF NOT EXISTS mesures (
    pir INTEGER,
    light INTEGER,
    sound INTEGER
  );
    CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    date_creation TEXT,
    matrice TEXT NOT NULL
  );
  CREATE TABLE IF NOT EXISTS config (
    mode TEXT NOT NULL,
    etat INTEGER NOT NULL,
    luminosite INTEGER NOT NULL,
    jeu_de_lumiere TEXT NOT NULL,
    couleur_actif TEXT NOT NULL,
    image_actif INTEGER,
    animation_actif TEXT,
    FOREIGN KEY(image_actif) REFERENCES images(id)
  );
  """)

  # Création des valeurs :

  # pour la table mesures :
  resultat = conn.execute("SELECT COUNT(*) FROM mesures")
  nb = resultat.fetchone()[0]
  if nb == 0 :
    conn.executemany("INSERT INTO mesures (pir, light, sound) VALUES (?, ?, ?)", (0,0,0))

  # pour la table images :
  resultat = conn.execute("SELECT COUNT(*) FROM images")
  nb = resultat.fetchone()[0]
  if nb == 0 :
    smiley = str([
      (255, 255, 255), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 255),
      (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0),
      (255, 255, 0), (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 255, 0), (255, 255, 255), (255, 255, 255), (255, 255, 0),
      (255, 255, 0), (255, 255, 255), (255, 255, 255), (255, 255, 0), (255, 255, 0), (0, 0, 0), (255, 255, 255), (255, 255, 0),
      (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0),
      (255, 255, 0), (0, 0, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (0, 0, 0), (255, 255, 0),
      (255, 255, 0), (255, 255, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 255), (255, 255, 0),
      (255, 255, 255), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 0, 255), (255, 0, 255), (255, 255, 255),
    ])
    conn.executemany("INSERT INTO images (nom, matrice) VALUES (?, ?)", ("smiley",smiley))

  # pour la table config :
  resultat = conn.execute("SELECT COUNT(*) FROM config")
  nb = resultat.fetchone()[0]
  if nb == 0 :
    conn.executemany("INSERT INTO config (mode,etat,luminosite,jeu_de_lumiere,couleur_actif) VALUES (?,?,?,?,?)", ("manual",0,30,"couleur","(255,255,255)"))
  conn.commit()
  conn.close()

if __name__ == "__main__":
  setup()
