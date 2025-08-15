import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            area TEXT,
            first_login INTEGER DEFAULT 1  -- 1 = primera vez, 0 = ya ingresó
        )
    ''')
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, password, area):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, area, first_login) VALUES (?, ?, ?, 1)',
              (username, hashed_password, area))
    conn.commit()
    conn.close()

def validate_login(username, password):
    user = get_user_by_username(username)
    if user:
        stored_hash = user[2]  # (id, username, password, area, first_login)
        if check_password_hash(stored_hash, password):
            # Si es primer login, devolver indicador
            return True, bool(user[4])  
    return False, False

def update_password(username, new_password):
    hashed_password = generate_password_hash(new_password)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # Cambiar contraseña y marcar que ya no es primer login
    c.execute('UPDATE users SET password = ?, first_login = 0 WHERE username = ?', 
              (hashed_password, username))
    conn.commit()
    conn.close()
