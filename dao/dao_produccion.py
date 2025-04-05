from utils import db
from models.produccion import Produccion
from models.detalle_produccion import DetalleProduccion
from models.pedido import Pedido, DetallePedido
from models.usuario import Usuario
from models.persona import Persona
from models.galleta import Galleta
from datetime import datetime
from sqlalchemy import func 
from flask import jsonify

def getAllConfirmaciones():
    confirmaciones = Produccion.query.filter(Produccion.estatus == 2).all()
    return confirmaciones

def getAllDetallesConfirmaciones(idProduccion):
    detalleConfirmacion = db.session.query(
        Produccion.id_produccion,
        Galleta.id_galleta,
        Galleta.nombre_galleta,
        DetalleProduccion.cantidad
    ).select_from(Produccion)\
    .join(DetalleProduccion, Produccion.id_produccion == DetalleProduccion.id_produccion)\
    .join(Galleta, DetalleProduccion.id_galleta == Galleta.id_galleta)\
    .filter(Produccion.id_produccion == idProduccion)\
    .all()
    return detalleConfirmacion

def procesarProduccion(id_produccion):
    try:
        print(id_produccion)
        produccion = Produccion.query.filter(Produccion.id_produccion == id_produccion).first()
        print(produccion)
        if produccion != None:
            produccion.estatus = 3
            db.session.add(produccion)
            db.session.commit()
            return 1
    except Exception as exception:
        return -1

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
