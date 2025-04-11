from flask import Blueprint, render_template, request, jsonify
from dao import dao_produccion
from models.produccion import Produccion
from models.detalle_produccion import DetalleProduccion
from controller import controller_detalle_produccion, controller_produccion, controller_materia_prima
from datetime import date, datetime
from forms import DetalleRecetaForm
from controller.controller_cliente import ClienteController
from flask import Blueprint, render_template, request
from dao import dao_produccion
from models.Stock import Stock
from controller import controller_stock
from funcs import crear_log_error, crear_log_user
import os
from utils import Blueprint, render_template, redirect, flash, db, url_for, request, login_required, current_user, abort

cocina_pedidos_bp = Blueprint('cocina-pedidos', __name__, template_folder='templates')

@cocina_pedidos_bp.route('/cocina-pedidos')
@login_required
def cocina_pedidos():
    if current_user.rol_user not in [0, 3]:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        form = DetalleRecetaForm()
        pedidos = dao_produccion.obtenerPedidos()
        return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstPedidos = pedidos, form=form)
    except Exception as e:
        crear_log_error(current_user.usuario,'/cocina-pedidos')
        abort(404)

@cocina_pedidos_bp.route('/procesar-pedido', methods=['POST'])
@login_required
def procesarPedido():
    if current_user.rol_user not in [0, 3]:
        abort(404)
    os.system("clear")
    data = request.json
    lstDetallePedido = data.get('lst_detalles')
    
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
    
    for detalleProduccion in lstDetallePedido:
        objDetalleProduccion = DetalleProduccion()
        cantidad = detalleProduccion["cantidad"]
        tipoPedido = detalleProduccion["tipo_pedido"]
        id_galleta = detalleProduccion["id_galleta"]
        id_pedido = detalleProduccion["id_pedido"]

        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_galleta = id_galleta
        objDetalleProduccion.cantidad = calculaPiezasTipoPedido(cantidad, tipoPedido)
        if objDetalleProduccion.cantidad == 0:
            continue
        
        detalleProduccion = controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)
        if detalleProduccion == -1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al registrar el detalle de produccion!"
            })

        #Proceso - Materia
        materiaPrima = controller_materia_prima.descontarStock(id_galleta, cantidad)
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
        objStock.id_galleta = id_galleta
        objStock.cantidad_galleta = cantidad
        agregarStock = controller_stock.agregarStock(objStock)
        if agregarStock != 1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al actualizar el stock!"
            })
    
    #Proceso - Pedido
    if ClienteController.actualizarPedido(id_pedido) != 1:
        return jsonify({
                "error": True,
                "message": "Hubo un problema al actualizar el pedido!"
            })

    return jsonify({
                "success": True,
                "message": "Se envio correctamente a produccion!"
            })

def calculaPiezasTipoPedido(cantidad, tipoPedido):
    if tipoPedido == 'pieza':
        return cantidad
    if tipoPedido == 'paquete':
        piezasPaquete = 50
        return cantidad * piezasPaquete
    if tipoPedido == 'peso':
        piezasPeso = 10
        return cantidad * piezasPeso

@cocina_pedidos_bp.route('/pedidos-historial', methods=['GET'])
@login_required
def pedidosHistorial():
    if current_user.rol_user not in [0, 3]:
        abort(404)
    fecha = request.args.get('fecha')
    if fecha == None:
        fecha = date.today().strftime('%Y-%m-%d')
    pedidos = dao_produccion.obtenerPedidosProcesados(fecha)
    return render_template('pages/page-produccion/cocina-pedidos/historial.html', lstPedidos = pedidos, fecha = fecha)

@cocina_pedidos_bp.route('/detalles-pedido', methods=['GET'])
@login_required
def detallePedido():
    if current_user.rol_user not in [0, 3]:
        abort(404)
    form = DetalleRecetaForm()
    idPedido = request.args.get('idPedido')
    detallesPedido = dao_produccion.obtenerDetallePedidos(int(idPedido))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        detalles = [{
            'id_pedido': idPedido,
            'id_galleta': detalle.id_galleta,
            'nombre_galleta': detalle.nombre_galleta,
            'cantidad': detalle.cantidad,
            'tipo_pedido': detalle.tipo_pedido
        } for detalle in detallesPedido]
        return jsonify(detalles)
    
    pedidos = dao_produccion.obtenerPedidos()
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstPedidos=pedidos, detallesPedido=detallesPedido, form=form)