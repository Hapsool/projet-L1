import sqlite3
from config import DB_CAPTEURS, DB_SITE

def init_db(path, table_sql):
  connect = sqlite3.connect(path)
  connect.execute("PRAGMA journal_mode=WAL;")
  connect.execute(table_sql)
  connect.commit()
  connect.close()
  
def setup():
  pass

if __name__ == "__main__":
  setup()
