import hashlib

def hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()
