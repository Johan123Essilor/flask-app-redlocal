import sqlite3
from datetime import datetime

DB_PATH = 'shippingClose.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shippingClose (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                andenNo INTEGER,
                type TEXT NOT NULL,
                qty INTEGER,
                sellos TEXT,
                completo TEXT,
                destino TEXT,
                comentarios TEXT,
                usuario TEXT,              -- NUEVO campo para usuario/autor
                fecha_registro TEXT
            )
        ''')
        conn.commit()

def insert_shipping(andenNo, tipo, qty, sellos, completo, destino, comentarios, usuario):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO shippingClose (andenNo, type, qty, sellos, completo, destino, comentarios, usuario, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            andenNo,
            tipo,
            qty,
            sellos,
            completo,
            destino,
            comentarios,
            usuario,  # Insertamos el usuario aquí
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()

def get_all_shipping(filter_type=None, filter_destino=None, filter_completo=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM shippingClose WHERE 1=1'
        params = []

        if filter_type:
            query += ' AND type = ?'
            params.append(filter_type)
        if filter_destino:
            query += ' AND destino LIKE ?'
            params.append(f'%{filter_destino}%')
        if filter_completo:
            query += ' AND completo = ?'
            params.append(filter_completo)

        query += ' ORDER BY fecha_registro DESC'
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [
            dict(zip(['id', 'andenNo', 'type', 'qty', 'sellos', 'completo', 'destino', 'comentarios', 'usuario', 'fecha_registro'], row))
            for row in rows
        ]

def delete_shipping(record_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shippingClose WHERE id = ?', (record_id,))
        conn.commit()
        return cursor.rowcount > 0
