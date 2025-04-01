from dao import dao_detalle_produccion
from cqrs import cqrs_detalle_produccion
from models import detalle_produccion

import os

def agregarDetalleProduccion(detalleProduccion):
    detalleProduccion.id_detalle_produccion = cqrs_detalle_produccion.agregarDetalleProduccion(detalleProduccion)
    return detalleProduccion.id_detalle_produccion
