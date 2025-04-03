from utils import db
from models import Persona, Usuario, Empleado

def obtener_empleados():
    empleados = Empleado.query.join(Persona).join(Usuario).filter(Persona.estatus != 0, Usuario.rol_user != 1).all()
    return empleados

def obtener_empleado_especifico(id_empleado):
    return db.session.query(Empleado).filter(Empleado.id_empleado==id_empleado).first()

def guardar_info_persona(u):
    db.session.add(u)
    db.session.commit() 
    return u.id_persona

def guardar_info_usuario(u):
    db.session.add(u)
    db.session.commit() 
    return u.id

def guardar_info_empleado(u):
    db.session.add(u)
    db.session.commit() 
    return u.id_empleado != None
