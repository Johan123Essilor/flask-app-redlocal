import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_users():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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

def add_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

def validate_login(username, password):
    user = get_user_by_username(username)
    if user:
        stored_hash = user[2]  # user = (id, username, password_hash)
        return check_password_hash(stored_hash, password)
    return False
