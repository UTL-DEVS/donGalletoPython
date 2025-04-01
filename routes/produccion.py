from flask import Blueprint, request, jsonify
import json
from models import produccion, detalle_produccion
from controller import  controller_produccion, controller_detalle_produccion
from datetime import date, datetime

produccion_bp = Blueprint('produccion', __name__, template_folder='templates')

@produccion_bp.route('/agregarProduccion', methods=['POST'])
def agregarProduccion():
    data = request.get_json()
    objProduccion = produccion.Produccion()
    objProduccion.fecha_produccion = date.today().strftime('%Y-%m-%d')
    objProduccion.hora_produccion = datetime.now().strftime('%H:%M:%S')
    objProduccion.estatus = 1
    objProduccion.id_produccion = controller_produccion.agregarProduccion(objProduccion)
    lstDetalleProduccion = data.get('lstDetalleProduccion')
    for detalleProduccion in lstDetalleProduccion:
        objDetalleProduccion = detalle_produccion.DetalleProduccion()
        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_galleta = detalleProduccion["id_galleta"]
        objDetalleProduccion.cantidad = detalleProduccion["cantidad"]
        if objDetalleProduccion.cantidad == 0:
            continue
        resultadoDetalleProduccion = controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })

