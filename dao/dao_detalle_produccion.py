from utils import db
from models.produccion import Produccion
from models.galleta import Galleta
from models.detalle_produccion import DetalleProduccion
from datetime import date

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
    .all()

    datos_formateados = [{
        'fecha_produccion': res.fecha_produccion,
        'hora_produccion': res.hora_produccion,
        'nombre_galleta': res.nombre_galleta,
        'cantidad_galleta': res.cantidad
    } for res in resultados]

    return datos_formateados

def agregarDetalleProduccion(detalleProduccion):
    db.session.add(detalleProduccion)
    db.session.commit()
    actualizarCantidadGalletas(detalleProduccion)
    return detalleProduccion.id_detalle_produccion

def actualizarCantidadGalletas(detalleProduccion):
    galleta = Galleta.query.get(detalleProduccion.id_galleta)
    cantidad = detalleProduccion.cantidad
    if galleta:
        galleta.cantidad_galleta +=  cantidad
    else:
        raise ValueError(f"No se encontró la galleta con ID {detalleProduccion.id_galleta}")
    db.session.commit()