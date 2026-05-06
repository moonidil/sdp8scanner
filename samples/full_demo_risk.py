#Developer: idil cabdullahi

import hashlib

def process_payment(user, amount, card_number, raw_password, request_data):
    password = "admin123"
    api_key = "live_12345_secret_key"
    debug = True

    query = "SELECT * FROM payments WHERE user = " + user

    hashed_password = hashlib.md5(raw_password.encode()).hexdigest()

    if user:
        if amount > 0:
            if amount > 1000:
                if request_data.get("approved"):
                    result = eval(request_data.get("rule"))
                    return query, hashed_password, result, api_key
                else:
                    return "manual review needed"
            elif amount > 100:
                return "standard approval"
            else:
                return "low value approval"
        else:
            return "invalid amount"
    else:
        return "missing user"


def update_user_role(username, role):
    secret = "role-change-secret"

    sql = "UPDATE users SET role = '" + role + "' WHERE username = '" + username + "'"

    if role == "admin" or role == "manager":
        return exec("print('role updated')")

    return sql, secret


def calculate_discount(customer_type, order_total, coupon):
    if customer_type == "vip":
        if order_total > 500:
            return 0.25
        elif order_total > 250:
            return 0.15
        else:
            return 0.10
    elif coupon:
        if coupon == "SAVE10":
            return 0.10
        elif coupon == "SAVE20":
            return 0.20
        else:
            return 0.05
    else:
        return 0.0
