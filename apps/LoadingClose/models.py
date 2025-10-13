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
                caja_pacas TEXT,
                gaylord TEXT,
                truck_id TEXT,
                vuelta_en_u INTEGER DEFAULT 0,
                usuario TEXT,
                fecha_registro TEXT
            )
        ''')
        conn.commit()

def insert_shipping(andenNo, tipo, qty, sellos, completo, destino,
                    comentarios, caja_pacas, gaylord, truck_id,
                    vuelta_en_u, usuario):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO shippingClose (
                andenNo, type, qty, sellos, completo, destino,
                comentarios, caja_pacas, gaylord, truck_id, vuelta_en_u,
                usuario, fecha_registro
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            andenNo,
            tipo,
            qty,
            sellos,
            completo,
            destino,
            comentarios,
            caja_pacas,
            gaylord,
            truck_id,
            1 if vuelta_en_u else 0,   # Guardamos como 0/1
            usuario,
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
            dict(zip(
                [
                    'id', 'anden', 'tipo', 'cantidad', 'sellos',
                    'completo', 'destino', 'comentarios', 'encargado', 'fecha','caja_pacas',
                    'gaylord', 'truck_id', 'vuelta_en_u'
                ],
                row
            ))
            for row in rows
        ]

def delete_shipping(record_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shippingClose WHERE id = ?', (record_id,))
        conn.commit()
        return cursor.rowcount > 0
def toggle_vuelta_en_u_db(registro_id, nuevo_valor):
    """Actualiza el valor de vuelta_en_u de un registro específico"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE shippingClose SET vuelta_en_u = ? WHERE id = ?",
            (1 if nuevo_valor else 0, registro_id)
        )
        conn.commit()