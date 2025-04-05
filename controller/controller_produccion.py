from cqrs import cqrs_produccion

import os

def agregarProduccion(produccion):
    return cqrs_produccion.agregarProduccion(produccion)

def procesarProduccion(id_produccion):
    return cqrs_produccion.procesarProduccion(id_produccion)