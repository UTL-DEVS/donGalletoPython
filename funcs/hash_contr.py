import hashlib

def hash(contrasenia : str) -> str:
    hash_obj = hashlib.sha256(contrasenia.encode('utf-8'))
    has_pass = hash_obj.hexdigest()
    return has_pass