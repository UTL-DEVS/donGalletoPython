from utils import db
from models import Usuario, Empleado
from utils import session
import os
from datetime import datetime
from utils import redirect
from utils import login_user

from funcs import delate_captcha_session, verificar_captcha

def dao_login(usuario, contrasenia, captcha_data):
    os.system('cls')
    if not captcha_data:
        return False
    else:
        dato, captcha_txt= verificar_captcha()


from funcs import delate_captcha_session, verificar_captcha

def dao_login(usuario, contrasenia, captcha_data):
    
    
    
    if not captcha_data:
        
        return False
    else:
        dato, captcha_txt= verificar_captcha()
        if dato > 60:
            delate_captcha_session('captcha_txt')
            return False  # if was passed more to one minute don't leave pass
        if captcha_txt != captcha_data:
            return False
        else:
            datos =  verify_user(usuario=usuario, contrasenia=contrasenia)
            if datos:
                name_user = datos[0]
                rol_user = datos[1]
                if rol_user == 1:
                    return redirect('/cliente')
                elif rol_user == 0:
                    return redirect('/receta')
                elif rol_user == 3:
                    return redirect('/produccion-stock')
                elif rol_user == 4:
                     return redirect('/tipo_venta')
            else:
                return False
            
def verify_user(usuario, contrasenia):
        usuario_local = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasenia == contrasenia).first()
        if(verify_employee(usuario,contrasenia)): # Verifica si el usuario es un empleado y si ha sido desactivado
            return False
        if usuario_local:
                login_user(usuario_local)
                nombre_usuario = usuario_local.usuario
                rol_usuario = usuario_local.rol_user
                usuario_local.generar_token()  # Genera el token y lo guarda
                usuario_local.generar_ultimo_acceso()
                usuario_local.dentro_sistema()
                print([nombre_usuario, rol_usuario])

                session['usuario_id'] = usuario_local.id
                
                return [nombre_usuario, rol_usuario]
        
        else:
            return False

def verify_employee(usuario, contrasenia):
    usuario_local = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasenia == contrasenia).first()
    if not usuario_local:
        return False
    empleado_local = db.session.query(Empleado).filter(Empleado.id_usuario == usuario_local.id).first()
    if (empleado_local):
        return empleado_local.persona.estatus == 0 # True significa que el empleado ha sido desactivado
    else: 
        return False