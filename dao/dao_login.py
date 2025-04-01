from utils import db
from models import Usuario
from utils import session
import os
from datetime import datetime
from utils import redirect

<<<<<<< HEAD
from funcs import delate_captcha_session, verificar_captcha

def dao_login(usuario, contrasenia, captcha_data):
    os.system('cls')
    if not captcha_data:
        return False
    else:
        dato, captcha_txt= verificar_captcha()

=======

from funcs import delate_captcha_session, verificar_captcha

def dao_login(usuario, contrasenia, captcha_data):
    print(captcha_data)
    print('contrasenia dao')
    print(contrasenia)
    if not captcha_data:
        print(usuario, contrasenia, captcha_data)
        return False
    else:
        dato, captcha_txt= verificar_captcha()
>>>>>>> 4cd6ba1d49afb38c46c8679b99226b335fe7dbc4
        if dato > 60:
            delate_captcha_session('captcha_txt')
            return False  # if was passed more to one minute don't leave pass
        else:
            datos =  verify_user(usuario=usuario, contrasenia=contrasenia)
            if datos:
                name_user = datos[0]
                rol_user = datos[1]
                if rol_user == 1:
                    return redirect('/cliente')
<<<<<<< HEAD
                elif rol_user == 777:
                    return redirect('/cocina-produccion')
                
=======
                elif rol_user == 0:
                    return redirect('/receta')
>>>>>>> 4cd6ba1d49afb38c46c8679b99226b335fe7dbc4
            else:
                return False
            
def verify_user(usuario, contrasenia):
        usuario_local = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasenia == contrasenia).first()
        if usuario_local:
                nombre_usuario = usuario_local.usuario
                rol_usuario = usuario_local.rol_user
                usuario_local.generar_token()  # Genera el token y lo guarda
                usuario_local.generar_ultimo_acceso()
                usuario_local.dentro_sistema()
<<<<<<< HEAD
                os.system('cls')
=======
>>>>>>> 4cd6ba1d49afb38c46c8679b99226b335fe7dbc4
                print([nombre_usuario, rol_usuario])
                return [nombre_usuario, rol_usuario]
        else:
            return False
