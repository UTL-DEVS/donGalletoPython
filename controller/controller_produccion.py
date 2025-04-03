from cqrs import cqrs_produccion

import os

def agregarProduccion(produccion):
    return cqrs_produccion.agregarProduccion(produccion)