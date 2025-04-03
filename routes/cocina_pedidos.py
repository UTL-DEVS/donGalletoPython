from flask import Blueprint, render_template, request, jsonify
from dao import dao_produccion
from models.produccion import Produccion
from models.detalle_produccion import DetalleProduccion
from controller import controller_detalle_produccion, controller_produccion, controller_cliente
from datetime import date, datetime
from forms import DetalleRecetaForm
from controller.controller_cliente import ClienteController

cocina_pedidos_bp = Blueprint('cocina-pedidos', __name__, template_folder='templates')

@cocina_pedidos_bp.route('/cocina-pedidos')
def cocina_pedidos():
    form = DetalleRecetaForm()
    pedidos = dao_produccion.obtenerPedidos()
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstPedidos = pedidos, form=form)

@cocina_pedidos_bp.route('/pedidos-historial', methods=['GET'])
def pedidosHistorial():
    fecha = request.args.get('fecha')
    if fecha == None:
        fecha = date.today().strftime('%Y-%m-%d')
    print(fecha)
    pedidos = dao_produccion.obtenerPedidosProcesados(fecha)
    return render_template('pages/page-produccion/cocina-pedidos/historial.html', lstPedidos = pedidos)

@cocina_pedidos_bp.route('/detalles-pedido', methods=['GET'])
def detallePedido():
    form = DetalleRecetaForm()
    idPedido = request.args.get('idPedido')
    detallesPedido = dao_produccion.obtenerDetallePedidos(int(idPedido))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        detalles = [{
            'id_pedido': detalle.id_pedido,
            'id_galleta': detalle.id_galleta,
            'nombre_galleta': detalle.nombre_galleta,
            'cantidad': detalle.cantidad,
            'tipo_pedido': detalle.tipo_pedido
        } for detalle in detallesPedido]
        return jsonify(detalles)
    
    pedidos = dao_produccion.obtenerPedidos()
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html', lstPedidos=pedidos, detallesPedido=detallesPedido, form=form)

@cocina_pedidos_bp.route('/procesar-pedido', methods=['POST'])
def procesarPedido():
    data = request.get_json()
    idPedido = data.get('idPedido')
    lstDetallePedido = data.get('lstDetallePedido')
    
    objProduccion = Produccion()
    objProduccion.fecha_produccion = date.today().strftime('%Y-%m-%d')
    objProduccion.hora_produccion = datetime.now().strftime('%H:%M:%S')
    objProduccion.estatus = 1
    objProduccion.id_produccion = controller_produccion.agregarProduccion(objProduccion)
    for detalleProduccion in lstDetallePedido:
        objDetalleProduccion = DetalleProduccion()
        objDetalleProduccion.id_produccion = objProduccion.id_produccion
        objDetalleProduccion.id_galleta = detalleProduccion.get('id_galleta')
        cantidad = int(detalleProduccion.get('cantidad'))
        tipoPedido = detalleProduccion.get('tipo_pedido')
        
        
        objDetalleProduccion.cantidad = calculaPiezasTipoPedido(cantidad, tipoPedido)
        if objDetalleProduccion.cantidad == 0:
            continue
        controller_detalle_produccion.agregarDetalleProduccion(objDetalleProduccion)
    ClienteController.actualizarPedido(idPedido)

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