from dao import dao_detalle_produccion
from cqrs import cqrs_detalle_produccion
from models import detalle_produccion

import os

def agregarDetalleProduccion(detalleProduccion):
    return cqrs_detalle_produccion.agregarDetalleProduccion(detalleProduccion)