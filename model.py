ADMIN_USER="hackbright"
ADMIN_PASSWORD=803096023

def authenticate(username, password):
    if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
        return ADMIN_USER
    else:    
        return None
