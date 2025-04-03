from utils import db
from models.produccion import Produccion
from models.pedido import Pedido, DetallePedido
from models.usuario import Usuario
from models.persona import Persona
from models.galleta import Galleta
from datetime import datetime
from sqlalchemy import func 
from flask import jsonify


def getAllProduccion():
    produccion = Produccion.query.all()
    return produccion

def agregarProduccion(produccion):
    try:
        db.session.add(produccion)
        db.session.commit()
        return produccion.id_produccion 
    except Exception as exception:
        return -1

def obtenerPedidos():
    pedidos = db.session.query(
        Pedido.id_pedido,
        Pedido.fecha_pedido, 
        Pedido.estatus,
        Persona.nombre,
        Persona.primerApellido
    ).select_from(Pedido)\
    .join(Usuario, Pedido.id_usuario == Usuario.id)\
    .join(Persona, Usuario.id_persona == Persona.id_persona)\
    .filter(Pedido.estatus == 'en proceso')\
    .all()
    return pedidos

def obtenerPedidosProcesados(fecha):
    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
    pedidos = db.session.query(
        Pedido.id_pedido,
        Pedido.fecha_pedido, 
        Pedido.estatus,
        Persona.nombre,
        Persona.primerApellido
    ).select_from(Pedido)\
    .join(Usuario, Pedido.id_usuario == Usuario.id)\
    .join(Persona, Usuario.id_persona == Persona.id_persona)\
    .filter(Pedido.estatus == 'procesado')\
    .filter(func.date(Pedido.fecha_pedido) == fecha)\
    .all()
    print(pedidos)
    return pedidos

def obtenerDetallePedidos(idPedido):
    detallePedido = db.session.query(
        Pedido.id_pedido,
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        DetallePedido.cantidad,
        DetallePedido.tipo_pedido
    ).select_from(Pedido)\
    .join(DetallePedido, Pedido.id_pedido == DetallePedido.id_pedido)\
    .join(Galleta, DetallePedido.id_galleta == Galleta.id_galleta)\
    .filter(Pedido.id_pedido == idPedido)\
    .all()
    return detallePedido
