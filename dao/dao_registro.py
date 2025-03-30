from utils import db, session, redirect
from models import Usuario
import os
from datetime import datetime, timezone
import re
import base64
import secrets
from funcs import delate_captcha_session, verificar_captcha,  enviar_correo


password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'

def validar_contrasenia(contrasenia):
    return bool(re.fullmatch(password_regex, contrasenia))

def dao_registro(email, usuario, contrasenia, captcha):
    if not captcha:
        return False

    os.system('cls')
    
    if not validar_contrasenia(contrasenia):
        print("Contraseña no válida")
        return False
    
    dato, captcha_txt = verificar_captcha()
    if dato > 120: # segundos
        delate_captcha_session('captcha_txt')
        return False
    
    # Comprobar si el usuario ya existe
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        print("El correo ya está registrado")
        return False
    token_bytes = secrets.token_bytes(32)
    token = base64.b64encode(token_bytes).decode('utf-8')
    nuevo_usuario = Usuario(
        email=email,
        usuario=usuario,
        contrasenia=contrasenia,
        rol=0,
        sistema=0,
        token=token
    )
    enviar_correo(cuerpo='123', destino=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    print("Usuario registrado correctamente")
    return nuevo_usuario