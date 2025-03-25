from utils import db
from models import Usuario
from utils import session
import os
from datetime import datetime
from utils import redirect

from funcs import delate_captcha_session


def dao_login(usuario, contrasenia, captcha_data):
    os.system('cls')
    if not captcha_data:
        return False
    else:
        dato, captcha_txt= verificar_captcha()

        if dato > 30:
            delate_captcha_session('captcha_txt')
            return False  # if was passed more to one minute don't leave pass
        else:
            datos =  verify_user(usuario=usuario, contrasenia=contrasenia)
            if datos:
                name_user = datos[0]
                rol_user = datos[1]
                return rol_user
            else:
                return False
            
def verify_user(usuario, contrasenia):
        usuario_local = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasenia == contrasenia).first()
        if usuario_local:
                nombre_usuario = usuario_local.usuario
                rol_usuario = usuario_local.rol
                usuario_local.generar_token()  # Genera el token y lo guarda
                usuario_local.generar_ultimo_acceso()
                usuario_local.dentro_sistema()
                os.system('cls')
                print([nombre_usuario, rol_usuario])
                return [nombre_usuario, rol_usuario]
        else:
            return False

def verificar_captcha():
    captcha_txt = session.get('captcha_txt')
    captcha_time = session.get('captcha_time')
    
    if captcha_time.tzinfo is not None:
        captcha_time = captcha_time.replace(tzinfo=None)  # Convertirlo a naive (sin zona horaria)

    actual = datetime.now()


    captcha_time_minute = captcha_time.replace(second=0, microsecond=0)
    actual_minute = actual.replace(second=0, microsecond=0)


    dato = actual_minute - captcha_time_minute
    return dato.total_seconds(), captcha_txt