import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    connect_to_db()
    query = """SELECT username, password, id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    #row[0] is username, row[1] is password, row[2] is user id
    #temp fix changed password from database to int so it evaluates true
    if username == row[0] and hash(password) == int(row[1]):
        #returns user id
        return row[2]
    else:    
        return None


def get_user_by_name(username):
    connect_to_db()
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    #row[0] is user id
    return row[0]

def get_wall_by_user(user_id):
    connect_to_db()
    #working on this query still
    query = """SELECT username, content, created_at 
    FROM wall_posts JOIN users ON users.id = wall_posts.author_id  WHERE owner_id = ?"""
    DB.execute(query, (user_id,))
    posts = DB.fetchall()
    #posts[]
    return posts   


def post_to_wall(owner_id, author_id, content):
    connect_to_db()
    query = """INSERT into wall_posts (owner_id, author_id, content) 
    VALUES (?,?,?)"""  
    DB.execute(query,(owner_id, author_id, content,))
    CONN.commit()