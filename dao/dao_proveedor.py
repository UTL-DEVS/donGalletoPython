from utils import db
from models import Proveedor, Persona

def obtener_proveedores():
    proveedores = Proveedor.query.all()
    return proveedores

def obtener_proveedores_activos():
    proveedores = Proveedor.query.join(Persona).filter(Persona.estatus!=0).all()
    return proveedores

def obtener_proveedor_especifico(id_proveedor):
    return db.session.query(Proveedor).filter(Proveedor.id_proveedor==id_proveedor).first()

def actualizar_proveedor(prov):
    db.session.add(prov)
    db.session.commit()

def agregar_proveedor(prov):
    db.session.add(prov)
    db.session.commit()
    return prov.id_proveedor!=None

def agregar_persona_proveedor(persona_prov):
    db.session.add(persona_prov)
    db.session.commit()
    return persona_prov.id_persona
