from utils import db, session, redirect, flash
from models import Usuario, PreRegistro
import os
from datetime import datetime, timezone
import base64
import secrets
from funcs import delate_captcha_session, verificar_captcha,  enviar_correo
import random


def dao_registro(email_local, usuario, contrasenia, captcha):
    if not captcha:
        return False

    
   
    
    dato, captcha_txt = verificar_captcha()
    if dato > 120: # segundos
        delate_captcha_session('captcha_txt')
        return False
    
    # Verificar si el correo o el usuario ya existen
    usuario_existente = PreRegistro.query.filter_by(email=email_local).first()
    if usuario_existente:
        flash("El correo ya está registrado.", 'error')
        return False
    
    usuario_existente = PreRegistro.query.filter_by(usuario=usuario).first()
    if usuario_existente:
        flash("El nombre de usuario ya está registrado. Intenta con otro.", 'error')
        return False
    token_bytes = secrets.token_bytes(32)
    
    token = base64.b64encode(token_bytes).decode('utf-8')
    token_local = generarToken()
    nuevo_usuario = PreRegistro(
        usuario=usuario,
        email=email_local,
        token=token_local,
        contrasenia = contrasenia
    )

    print(nuevo_usuario.contrasenia)
    enviar_correo(cuerpo=f'{token_local} \n para poder confirmar ingresar a: http://localhost:8080/confirmar', destino=email_local)
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    print("Usuario registrado correctamente")
    return nuevo_usuario


def generarToken():
    token = random.randint(11111,99999)
    return token

def dao_conf(email, token):
    
    
    
    usuario_local = PreRegistro.query.filter_by(email=email).first()
    usuario_guardado = Usuario.query.filter_by(email=email).first()
    if usuario_local and usuario_local.token == token and not usuario_guardado:
        usuario_final = Usuario(
            usuario = usuario_local.usuario,
            email=email,
            contrasenia = usuario_local.contrasenia,
            rol_user = 1,
            sistema = 1,
            token = generarToken()
        )
        print('usuarioGuardado')
        db.session.add(usuario_final)
        db.session.commit()
        return redirect('/cliente')
    return False