from cqrs import cqrs_login
from dao import dao_login
import os
def controller_login(usuario, contrasenia):
    if cqrs_login(usuario, contrasenia):
        os.system('cls')
        print(usuario, contrasenia)
        datos = dao_login(usuario, contrasenia)
        nombre_usuario, rol_usuario, token_usuario = datos
        if nombre_usuario and rol_usuario:
            return f'{nombre_usuario} rol: {rol_usuario}, token:{token_usuario}'
        else: None