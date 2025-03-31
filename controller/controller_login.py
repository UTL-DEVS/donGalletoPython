from cqrs import cqrs_login
from dao import dao_login
import os
import bcrypt



def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def controller_login(usuario, contrasenia, captcha_data):
    hashed_password = hash_password(contrasenia)
    return cqrs_login(usuario, hashed_password, captcha_data)