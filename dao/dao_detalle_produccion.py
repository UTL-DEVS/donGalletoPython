from utils import db
from models.produccion import Produccion
from models.galleta import Galleta
from models.detalle_produccion import DetalleProduccion
from datetime import date
from flask import jsonify

def obtenerDetalleProduccion(fecha):
    resultados = db.session.query(
        Produccion.fecha_produccion,
        Produccion.hora_produccion,
        Galleta.nombre_galleta,
        DetalleProduccion.cantidad
    ).select_from(Produccion)\
    .join(DetalleProduccion)\
    .join(Galleta)\
    .filter(Produccion.fecha_produccion == fecha)\
    .filter(Produccion.estatus == 3)\
    .all()

    datos_formateados = [{
        'fecha_produccion': res.fecha_produccion,
        'hora_produccion': res.hora_produccion,
        'nombre_galleta': res.nombre_galleta,
        'cantidad_galleta': res.cantidad
    } for res in resultados]

    return datos_formateados

def agregarDetalleProduccion(detalleProduccion):
    try: 
        db.session.add(detalleProduccion)
        db.session.commit()
        return 1
    except Exception as exception:
        return -1

