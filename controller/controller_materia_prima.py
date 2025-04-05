from cqrs import cqrs_materia_prima
from models.materiaPrima import MateriaPrima

def actualizarStock(lstSolicitudes):
    try:
        for solicitud in lstSolicitudes:
            materia = MateriaPrima()
            materia.id_materia = solicitud.get('id_materia')
            materia.stock_materia = solicitud.get('cantidad')
            if cqrs_materia_prima.actualizarStock(materia) != 1:
                return -1
        return 1
    except Exception as exception:
        return -1
    
def descontarStock(idGalleta, cantidad):
    return cqrs_materia_prima.descontarStock(idGalleta, cantidad)