from flask import Blueprint, render_template, request, jsonify
from utils import Blueprint, render_template, redirect, flash, db, url_for, request, login_required, current_user, abort
from dao import dao_galleta, dao_detalle_produccion, dao_stock
from dao import dao_detalle_produccion, dao_resumen_venta
from forms import DetalleRecetaForm
from datetime import date, datetime
from models.detalle_produccion import DetalleProduccion
from models.produccion import Produccion
from models.Stock import Stock
from controller import controller_produccion, controller_detalle_produccion, controller_stock

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
def working():
    return render_template('pages/page-produccion/working-page.html')

@cocina_produccion_bp.route('/produccion')
@login_required
def produccion():
    if current_user.rol_user != 3:
        abort(404)
    form = DetalleRecetaForm()
    lstGalletas = dao_stock.obtenerStock()
    print(lstGalletas)
    return render_template('pages/page-produccion/cocina-produccion/stock.html', lstGalletas = lstGalletas, form = form)

@cocina_produccion_bp.route('/produccion-stock')
@login_required
def stock():
    if current_user.rol_user != 3:
        abort(404)
    form = DetalleRecetaForm()
    lstGalletas = dao_stock.obtenerStock()
    return render_template('pages/page-produccion/cocina-produccion/stock.html', lstGalletas = lstGalletas, form = form)

@cocina_produccion_bp.route('/produccion-historial', methods=['GET'])
@login_required
def historial():
    if current_user.rol_user != 3:
        abort(404)
    fecha = request.args.get('fecha')
    if fecha == None:
        fecha = date.today().strftime('%Y-%m-%d')
    lstGalletas = dao_detalle_produccion.obtenerDetalleProduccion(fecha)
    return render_template('pages/page-produccion/cocina-produccion/historial.html', lstGalletas = lstGalletas, fecha = fecha)

@cocina_produccion_bp.route('/procesar-produccion', methods=['POST'])
@login_required
def procesarProduccion():
    if current_user.rol_user != 3:
        abort(404)
    data = request.get_json()
    lstDetalleProduccion = data.get('lstDetalleProduccion')

    #Proceso - Produccion
    objProduccion = Produccion()
    objProduccion.fecha_produccion = date.today().strftime('%Y-%m-%d')
    objProduccion.hora_produccion = datetime.now().strftime('%H:%M:%S')
    objProduccion.estatus = 1
    objProduccion.id_produccion = controller_produccion.agregarProduccion(objProduccion)
    if objProduccion.id_produccion == -1:
        return jsonify({
                "error": True,
                "message": "Hubo un problema al registrar la produccion!"
            })

    #Proceso - DetalleProduccion
    for detalleProduccion in lstDetalleProduccion:
        objDetalleProduccion = DetalleProduccion()
        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_galleta = detalleProduccion["id_galleta"]
        objDetalleProduccion.cantidad = int(detalleProduccion["cantidad"])
        if objDetalleProduccion.cantidad == 0:
            continue
        if controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion) == -1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al registrar el detalle de produccion!"
            })
        
        #Proceso - Stock
        objStock = Stock()
        objStock.id_galleta = detalleProduccion["id_galleta"]
        objStock.cantidad_galleta = int(detalleProduccion["cantidad"])
        if controller_stock.agregarStock(objStock) != 1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al actualizar el stock!"
            })

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })