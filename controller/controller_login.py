from cqrs import cqrs_login
from dao import dao_login
import os
import bcrypt

def controller_login(usuario, contrasenia, captcha_data):
    print(captcha_data)
    print('contrasenia controller')
    print(contrasenia)
    return cqrs_login(usuario, contrasenia, captcha_data)