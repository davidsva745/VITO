import sqlite3

# Připojení k SQLite databázi (vytvoří ji, pokud neexistuje)
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Vytvoření tabulky visits
c.execute("""
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    timestamp DATETIME NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Tabulka visits byla úspěšně vytvořena.")
