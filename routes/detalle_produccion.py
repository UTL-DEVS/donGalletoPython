from flask import Blueprint, request
import json
from models import detalle_produccion
from controller import controller_detalle_produccion

detalle_produccion_bp = Blueprint('detalle-produccion', __name__, template_folder='templates')

@detalle_produccion_bp.route('/agregarDetalleProduccion', methods=['POST'])
def agregarDetalleProduccion():
    lstDetalleProduccion = request.args.get('lstDetalleProduccion')
    for detalleProduccion in lstDetalleProduccion:
        objDetalleProduccion = detalle_produccion()
        objDetalleProduccion.id_receta = detalleProduccion.id_receta
        objDetalleProduccion.id_produccion = detalleProduccion.id_produccion
        objDetalleProduccion.cantidad = detalleProduccion.cantidad
        controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)