from flask import Blueprint, render_template, request, jsonify
from utils import Blueprint, render_template, request, login_required, current_user, abort
from dao import dao_produccion, dao_detalle_produccion, dao_stock
from forms import DetalleRecetaForm
from datetime import date, datetime
from models.detalle_produccion import DetalleProduccion
from models.produccion import Produccion
from models.Stock import Stock
from controller import controller_produccion, controller_detalle_produccion, controller_stock, controller_materia_prima

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
def working():
    return render_template('pages/page-produccion/working-page.html')

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
    data = request.json
    lstDetalleProduccion = data.get('lstDetalleProduccion')

    #Proceso - Produccion
    objProduccion = Produccion()
    objProduccion.fecha_produccion = date.today().strftime('%Y-%m-%d')
    objProduccion.hora_produccion = datetime.now().strftime('%H:%M:%S')
    objProduccion.estatus = 2 #Por confirmar
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
        
        #Proceso - Detalle
        if controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion) == -1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al registrar el detalle de produccion!"
            })

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })

@cocina_produccion_bp.route('/produccion-confirmaciones')
@login_required
def confirmaciones():
    if current_user.rol_user != 3:
        abort(404)
    form = DetalleRecetaForm()
    lstConfirmaciones= dao_produccion.getAllConfirmaciones()
    return render_template('pages/page-produccion/cocina-produccion/confirmaciones.html', lstConfirmaciones = lstConfirmaciones, form = form)

@cocina_produccion_bp.route('/detalles-confirmacion', methods=['GET'])
@login_required
def detalleConfirmacion():
    if current_user.rol_user != 3:
        abort(404)
    form = DetalleRecetaForm()
    idProduccion = request.args.get('idProduccion')
    detallesConfirmacion = dao_produccion.getAllDetallesConfirmaciones(int(idProduccion))
    confirmaciones = dao_produccion.getAllConfirmaciones()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        detalles = [{
            'id_produccion': detalle.id_produccion,
            'nombre_galleta': detalle.nombre_galleta,
            'cantidad': detalle.cantidad,
            'id_galleta': detalle.id_galleta
        } for detalle in detallesConfirmacion]
        return jsonify(detalles)
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstConfirmaciones=confirmaciones, lstDetallesConfirmacion=detallesConfirmacion, form=form)

@cocina_produccion_bp.route('/confirmar-produccion', methods=['POST'])
@login_required
def confirmarProduccion():
    if current_user.rol_user != 3:
        abort(404)
    data = request.json
    lstDetalleProduccion = data.get('lstDetalleProduccion')
    id_produccion = data.get('id_produccion')

    #Proceso - Produccion
    produccion = controller_produccion.procesarProduccion(id_produccion)
    print('produccion ' + str(produccion))
    if produccion != 1:
        return jsonify({
                "error": True,
                "message": "Hubo un problema al buscar el pedido!"
            })

    #Proceso - DetalleProduccion
    for detalleProduccion in lstDetalleProduccion:
        #Proceso - Materia
        materiaPrima = controller_materia_prima.descontarStock(detalleProduccion["id_galleta"], int(detalleProduccion["cantidad"]))
        print('materia ' + str(materiaPrima))
        if materiaPrima != 1:
            if materiaPrima == -1:
                return jsonify({
                    "error": True,
                    "message": "Hubo un problema al descontar la materia!"
                })
            if materiaPrima == -3:
                return jsonify({
                    "error": True,
                    "message": "No tiene suficiente materia prima para producir!"
                })

        #Proceso - Stock
        objStock = Stock()
        objStock.id_galleta = detalleProduccion["id_galleta"]
        objStock.cantidad_galleta = int(detalleProduccion["cantidad"])
        stock = controller_stock.agregarStock(objStock)
        print('stock ' + str(stock))
        if stock != 1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al actualizar el stock!"
            })

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })