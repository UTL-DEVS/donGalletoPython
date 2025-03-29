from utils import db
from models import Proveedor

def obtener_proveedores():
    proveedores = Proveedor.query.all()
    return proveedores

def obtener_proveedor_especifico(id_proveedor):
    return db.session.query(Proveedor).filter(Proveedor.id_proveedor==id_proveedor).first()

def actualizar_proveedor(prov):
    db.session.add(prov)
    db.session.commit()
