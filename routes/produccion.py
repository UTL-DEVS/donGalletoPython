from flask import Blueprint, request
import json
from models import produccion, detalle_produccion
from controller import  controller_produccion, controller_detalle_produccion
from datetime import date

produccion_bp = Blueprint('produccion', __name__, template_folder='templates')

@produccion_bp.route('/agregarProduccion', methods=['POST'])
def agregarProduccion():
    fecha_produccion = date.today()
    objProduccion = produccion()
    objProduccion.fecha_produccion = fecha_produccion
    objProduccion.estatus = 1
    objProduccion.id_produccion = controller_produccion.agregarProduccion(objProduccion)
    lstDetalleProduccion = request.args.get('lstDetalleProduccion')
    for detalleProduccion in lstDetalleProduccion:
        objDetalleProduccion = detalle_produccion()
        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_receta = detalleProduccion.id_receta
        objDetalleProduccion.id_produccion = detalleProduccion.id_produccion
        objDetalleProduccion.cantidad = detalleProduccion.cantidad
        resultadoDetalleProduccion = controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)

        if resultadoDetalleProduccion != 1:
            return resultadoDetalleProduccion
        
    return objProduccion.id_produccion
