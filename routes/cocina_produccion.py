from flask import Blueprint, render_template, request, jsonify
from utils import login_required, current_user, redirect
from dao import dao_galleta, dao_detalle_produccion, dao_produccion
from forms import DetalleRecetaForm
from datetime import date, datetime
from models.detalle_produccion import DetalleProduccion
from models.produccion import Produccion
from controller import controller_produccion, controller_detalle_produccion

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
def working():
    return render_template('pages/page-produccion/working-page.html')

@cocina_produccion_bp.route('/produccion')
def produccion():
    form = DetalleRecetaForm()
    lstGalletas = dao_galleta.getAllGalletas()
    return render_template('pages/page-produccion/cocina-produccion/stock.html', lstGalletas = lstGalletas, form = form)

@cocina_produccion_bp.route('/produccion-stock')
def stock():
    form = DetalleRecetaForm()
    lstGalletas = dao_galleta.getAllGalletas()
    return render_template('pages/page-produccion/cocina-produccion/stock.html', lstGalletas = lstGalletas, form = form)

@cocina_produccion_bp.route('/produccion-historial', methods=['GET'])
def historial():
    fecha = request.args.get('fecha')
    if fecha == None:
        fecha = date.today().strftime('%Y-%m-%d')
    lstGalletas = dao_detalle_produccion.obtenerDetalleProduccion(fecha)
    return render_template('pages/page-produccion/cocina-produccion/historial.html', lstGalletas = lstGalletas, fecha = fecha)

@cocina_produccion_bp.route('/procesar-produccion', methods=['POST'])
def procesarProduccion():
    data = request.get_json()
    objProduccion = Produccion()
    objProduccion.fecha_produccion = date.today().strftime('%Y-%m-%d')
    objProduccion.hora_produccion = datetime.now().strftime('%H:%M:%S')
    objProduccion.estatus = 1
    objProduccion.id_produccion = controller_produccion.agregarProduccion(objProduccion)
    lstDetalleProduccion = data.get('lstDetalleProduccion')
    for detalleProduccion in lstDetalleProduccion:
        objDetalleProduccion = DetalleProduccion()
        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_galleta = detalleProduccion["id_galleta"]
        objDetalleProduccion.cantidad = int(detalleProduccion["cantidad"])
        if objDetalleProduccion.cantidad == 0:
            continue
        resultadoDetalleProduccion = controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })