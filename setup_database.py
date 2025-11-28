import sqlite3
from config import DB_PATH, NUM_LEDS

def setup():
  conn = sqlite3.connect(DB_PATH)
  conn.execute("PRAGMA journal_mode=WAL;")

  # Créations des tables si elles n'existes pas :
  conn.executescript("""
  CREATE TABLE IF NOT EXISTS mesures (
    pir INTEGER DEFAULT NULL,
    light INTEGER DEFAULT NULL,
    sound INTEGER DEFAULT NULL,
  );
    CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    date_creation TEXT,
    matrice TEXT NOT NULL
  );
  CREATE TABLE IF NOT EXISTS config (
    mode TEXT NOT NULL DEFAULT "manual",
    luminosite INTEGER NOT NULL DEFAULT 30,
    jeu_de_lumiere TEXT NOT NULL DEFAULT "couleur",
    couleur_actif TEXT NOT NULL DEFAULT "(255,255,255)",
    image_actif INTEGER DEFAULT NULL,
    animation_actif TEXT DEFAULT NULL,
    FOREIGN KEY(image_actif) REFERENCES images(id)
  );
  """)

  # insertion d'une image pour la table images :
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
    conn.executemany("INSERT INTO images (nom, matrice) VALUES (?, ?, ?)", ("smiley",smiley))

  conn.commit()
  conn.close()

if __name__ == "__main__":
  setup()
