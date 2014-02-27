import sqlite3

DB = None
CONN = None

def connect_to_db():
    """Create a connection with the database."""
    # TODO: When do we close this connection?
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    """Check a username/password"""
    connect_to_db()
    query = """SELECT username, password, id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()

    #row[0] is username, row[1] is password, row[2] is user id
    # if row exists, username matches and hashed password matches, return id
    # must cast password from db as int because it's stored as a string
    if row and username == row[0] and hash(password) == int(row[1]):
        #returns user id
        return row[2]
    else:    
        return None


def get_user_by_name(username):
    """Look up the user_id for a username"""
    connect_to_db()
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    #row[0] is user id
    if row == None:
        return None
    else:
        return row[0]

def get_name_by_user(user_id):
    """Look up the username for a user_id"""
    connect_to_db()
    query = """SELECT username FROM users WHERE id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    CONN.close()
    if row:
        return row[0]
    else:
        return None

def get_wall_by_user(user_id):
    """Fetch all the posts on a user's wall."""
    connect_to_db()
    query = """SELECT username, content, created_at 
    FROM wall_posts JOIN users ON users.id = wall_posts.author_id  WHERE owner_id = ? ORDER BY created_at DESC"""
    DB.execute(query, (user_id,))
    posts = DB.fetchall()
    CONN.close()
    return posts   


def post_to_wall(owner_id, author_id, content, current_datetime):
    """Post to a user's wall."""
    connect_to_db()
    query = """INSERT into wall_posts (owner_id, author_id, content, created_at) 
    VALUES (?,?,?, ?)"""  
    DB.execute(query,(owner_id, author_id, content, current_datetime))
    CONN.commit()
    CONN.close()


def make_new_user(username, password):
    """Add a new user in the database."""
    # password gets stored as the hash of password security yah.
    password = hash(password)
    connect_to_db()
    query = """INSERT into users (username, password) 
    VALUES (?,?)"""  
    DB.execute(query,(username, password,))
    CONN.commit()   
    CONN.close() 