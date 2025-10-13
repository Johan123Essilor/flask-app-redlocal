import sqlite3
from datetime import datetime

DB_PATH = 'VisualAID.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS VisualAID (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                cliente TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                creator TEXT NOT NULL,
                codigo TEXT NOT NULL
            )
        ''')
        conn.commit()


def insert_file(filename, original_name, cliente, creator, codigo):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO VisualAID (filename, original_name, cliente, upload_date, creator, codigo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            original_name,
            cliente,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            creator,
            codigo
        ))
        conn.commit()


def get_all_files(filter_cliente=None, filter_author=None, filter_name=None, filter_codigo=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = '''
            SELECT id, filename, original_name, cliente, upload_date, creator, codigo 
            FROM VisualAID 
            WHERE 1=1
        '''
        params = []

       
        if filter_cliente:
            query += ' AND cliente LIKE ?'
            params.append(f'%{filter_cliente}%')

        if filter_author:
            query += ' AND creator LIKE ?'
            params.append(f'%{filter_author}%')

        if filter_name:
            query += ' AND original_name LIKE ?'
            params.append(f'%{filter_name}%')

        if filter_codigo:
            query += ' AND codigo LIKE ?'
            params.append(f'%{filter_codigo}%')

        query += ' ORDER BY upload_date DESC'

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(zip(
            ['id', 'filename', 'original_name', 'cliente', 'upload_date', 'creator', 'codigo'],
            row
        )) for row in rows]


def delete_file(file_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM VisualAID WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        if result:
            filename = result[0]
            cursor.execute('DELETE FROM VisualAID WHERE id = ?', (file_id,))
            conn.commit()
            return filename
        return None


def update_file(file_id, new_name, new_cliente, new_codigo, new_filename=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if new_filename:
            cursor.execute('''
                UPDATE VisualAID
                SET original_name = ?, cliente = ?, codigo = ?, filename = ?
                WHERE id = ?
            ''', (new_name, new_cliente, new_codigo, new_filename, file_id))
        else:
            cursor.execute('''
                UPDATE VisualAID
                SET original_name = ?, cliente = ?, codigo = ?
                WHERE id = ?
            ''', (new_name, new_cliente, new_codigo, file_id))
        conn.commit()
