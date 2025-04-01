from dao import dao_produccion

def validarDatos(produccion):
    if produccion.fecha_produccion == '':
        return 'Hubo un problema al agregar la produccion, intentelo de nuevo!'
    if produccion.estatus == '':
        return 'Hubo un problema al asignar el estatus, intentelo de nuevo!'
    
    return ''

def agregarProduccion(produccion):
    validacionDatos = validarDatos(produccion)
    if validacionDatos != '':
        return validacionDatos
    
    return dao_produccion.agregarProduccion(produccion)    
