from dao import dao_detalle_produccion

def validarDatos(detalleProduccion):
    if detalleProduccion.id_produccion == '':
        return 'Hubo un problema al agregar la produccion, intentelo de nuevo!'
    if detalleProduccion.id_galleta == '':
        return 'Hubo un problema al relacionar la receta, intentelo de nuevo!'
    
    return ''

def agregarDetalleProduccion(detalleProduccion):
    validacionDatos = validarDatos(detalleProduccion)
    if validacionDatos != '':
        return -1
    
    return dao_detalle_produccion.agregarDetalleProduccion(detalleProduccion)    
