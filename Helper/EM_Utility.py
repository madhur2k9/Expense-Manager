import hashlib

def hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def recalc_current_balance(transac_type, transac_amount, current_balance):
    current_balance = float(current_balance)
    transac_amount = float(transac_amount)
    transac_type = bool(transac_type)
    if transac_type:
        current_balance += transac_amount
        return current_balance
    current_balance -= transac_amount
    return (current_balance)