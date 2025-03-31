from utils import db
from models import produccion, receta, detalle_produccion

def obtenerDetalleProduccion(idProduccion):
    return db.session.query(detalle_produccion).filter(detalle_produccion.id_produccion == idProduccion).first()

def agregarDetalleProduccion(detalleProduccion):
    db.session.add(detalleProduccion)
    db.session.commit()
    return detalleProduccion.id_detalle_produccion != None
