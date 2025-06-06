from cqrs import  cqrs_registro,  cqrs_conf
import re
import os
from utils import  redirect, flash
from funcs import hash
password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'

def validar_contrasenia(contrasenia):
    return bool(re.fullmatch(password_regex, contrasenia))

def controller_registro(email, usuario, contrasenia, captcha):
    if not validar_contrasenia(contrasenia):
        
        flash('Contraseña incorrecta. Debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.', 'error')
        
        return False
    print('contrasenia controller_login')
    print(contrasenia)
    contrasenia_hash = hash(contrasenia)
    return cqrs_registro(email, usuario, contrasenia_hash, captcha)

def controller_conf(email, token):
    return cqrs_conf(email, token)