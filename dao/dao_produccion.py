from utils import db
from models import produccion
from models.pedido import Pedido
from models.usuario import Usuario

def getAllProduccion():
    produccion = produccion.query.all()
    return produccion

# def obtener_proveedores_activos():
#     proveedores = produccion.query.join(Persona).filter(Persona.estatus!=0).all()
#     return proveedores

# def obtener_proveedor_especifico(id_proveedor):
#     return db.session.query(Proveedor).filter(Proveedor.id_proveedor==id_proveedor).first()

def agregarProduccion(produccion):
    db.session.add(produccion)
    db.session.commit()
    return produccion.id_produccion 

def obtenerPedidos():
    pedidos = db.session.query(
        Pedido.fecha_pedido, Pedido.estatus
    ).select_from(Pedido)\
    .all()
    return pedidos
