import sqlite3
from datetime import datetime

DB_PATH = 'sop_files.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sop_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT NOT NULL,
                area TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                creator TEXT NOT NULL
            )
        ''')
        conn.commit()


def insert_file(filename, original_name, area, creator):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sop_files (filename, original_name, area, upload_date, creator)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            filename,
            original_name,
            area,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            creator
        ))
        conn.commit()

def get_all_files(filter_area=None, filter_author=None, filter_name=None):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = 'SELECT id, filename, original_name, area, upload_date, creator FROM sop_files WHERE 1=1'
        params = []

        if filter_area:
            query += ' AND area = ?'
            params.append(filter_area)
        if filter_author:
            query += ' AND creator LIKE ?'
            params.append(f'%{filter_author}%')
        if filter_name:
            query += ' AND original_name LIKE ?'
            params.append(f'%{filter_name}%')

        query += ' ORDER BY upload_date DESC'

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(zip(['id', 'filename', 'original_name', 'area', 'upload_date', 'creator'], row)) for row in rows]

def delete_file(file_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM sop_files WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        if result:
            filename = result[0]
            cursor.execute('DELETE FROM sop_files WHERE id = ?', (file_id,))
            conn.commit()
            return filename
        return None
