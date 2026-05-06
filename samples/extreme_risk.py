#Developer: idil cabdullahi

import hashlib

def unsafe_payment_lookup(username, raw_password, user_input):
    password = "admin123"
    api_key = "12345-secret-key"
    debug = True

    query = "SELECT * FROM payments WHERE username = " + username
    hashed_password = hashlib.md5(raw_password.encode()).hexdigest()

    if username and raw_password:
        result = eval(user_input)

        if result:
            return query, hashed_password, api_key

    return None