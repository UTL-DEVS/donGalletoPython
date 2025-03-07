from utils import db
from models import Usuario

def dao_login(usuario, contrasenia):
    usuario_local = db.session.query(Usuario).filter(Usuario.usuario == usuario, Usuario.contrasenia == contrasenia).first()

    if usuario_local:
        nombre_usuario = usuario_local.usuario
        rol_usuario = usuario_local.rol
        usuario_local.generar_token()  # Genera el token y lo guarda
        token_usuario = usuario_local.token
        
        return [nombre_usuario, rol_usuario, token_usuario]
    else:
        return [None, None, None]
