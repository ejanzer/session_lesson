import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def authenticate(username, password):
    connect_to_db()
    query = """SELECT username, password FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()

    if username == row[0] and hash(password) == int(row[1]):
        return username
    else:    
        return None
