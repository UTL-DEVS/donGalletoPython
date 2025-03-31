from cqrs import cqrs_produccion

import os

def agregarProduccion(produccion):
    produccion.id_produccion = cqrs_produccion.agregarProduccion(produccion)
    return produccion.id_produccion