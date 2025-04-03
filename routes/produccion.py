from flask import Blueprint, request, jsonify, abort, login_required, current_user
import json
from models import produccion, detalle_produccion
from controller import  controller_produccion, controller_detalle_produccion
from datetime import date, datetime
from funcs import crear_log_user, crear_log_error


produccion_bp = Blueprint('produccion', __name__, template_folder='templates')

@produccion_bp.route('/agregarProduccion', methods=['POST'])
@login_required
def agregarProduccion():
    if current_user.rol_user != 2:
        abort(404)

    try:
        crear_log_user(current_user.usuario, request.url)

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
            controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)

        return jsonify({
            "success": True,
            "message": "Se envió correctamente a producción!"
        })

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return jsonify({
            "success": False,
            "message": "❌ Error al procesar producción.",
            "error": str(e)
        }), 500

