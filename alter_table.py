import sqlite3

DB_PATH = 'shippingClose.db'

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    # Intentamos agregar cada columna por separado
    try:
        cursor.execute("ALTER TABLE shippingClose ADD COLUMN gaylord TEXT")
        print("✅ Columna 'gaylord' agregada correctamente")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Error 'gaylord': {e}")

    try:
        cursor.execute("ALTER TABLE shippingClose ADD COLUMN truck_id TEXT")
        print("✅ Columna 'truck_id' agregada correctamente")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Error 'truck_id': {e}")

    try:
        cursor.execute("ALTER TABLE shippingClose ADD COLUMN vuelta_en_u INTEGER NOT NULL DEFAULT 0")
        print("✅ Columna 'vuelta_en_u' agregada correctamente")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Error 'vuelta_en_u': {e}")
