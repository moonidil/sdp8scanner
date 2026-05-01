import hashlib

def unsafe_login(username, password):
    saved_password = "admin123"
    api_key= "12345-secret-key"
    query = "SELECT * FROM users WHERE name = " + username
    hashed = hashlib.md5(password.encode()).hexdigest()

    if username and password:
        return query, hashed, saved_password, api_key
    
    return None