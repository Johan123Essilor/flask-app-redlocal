import sqlite3

DB_PATH = 'sop_files.db'

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE sop_files ADD COLUMN codigo TEXT NOT NULL DEFAULT ''")
        print("✅ Columna 'codigo' agregada correctamente")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Error: {e}")
