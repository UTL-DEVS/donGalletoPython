from dao import dao_insumos

def validarDatos(solicitud):
    if solicitud.id_materia == '':
        return 'Debe seleccionar una materia'
    if solicitud.stock_materia < 0:
        return 'Debe seleccionar mas de una pieza'
    return ''

def actualizarStock(solicitud):
    validacionDatos = validarDatos(solicitud)
    if validacionDatos != '':
        print(solicitud.id_materia)
        print(solicitud.stock_materia)

        return -1
    
    return dao_insumos.actualizarStock(solicitud)

def descontarStock(idGalleta, cantidad):
    print('cqrs-id '+idGalleta)
    print('cqrs-cnt '+str(cantidad))
    return dao_insumos.descontarStock(idGalleta, cantidad)