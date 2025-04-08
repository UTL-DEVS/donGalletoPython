from flask import Blueprint, render_template, request, jsonify
from datetime import date, timedelta
from forms import DetalleRecetaForm
from models.compra_insumos import CompraInsumo
from models.compra_insumos import DetalleCompraInsumo
from controller import controller_materia_prima
from dao import dao_insumos, dao_compra_insumo, dao_detalle_compra_insumo
from funcs import crear_log_error, crear_log_user
from utils import Blueprint, render_template, redirect, flash, db, url_for, request, login_required, current_user, abort
from utils.db import db

cocina_insumos_bp = Blueprint('cocina-insumos', __name__, template_folder='templates')

@cocina_insumos_bp.route('/cocina-insumos')
@login_required
def cocina_insumos():
    if current_user.rol_user != 3:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        form = DetalleRecetaForm()
        insumos = dao_insumos.obtenerInsumos()
        return render_template('pages/page-produccion/cocina-insumos/stock.html', lstInsumos = insumos, form=form)
    except Exception as e:
        crear_log_error(current_user.usuario,'/cocina-pedidos')
        abort(404)

@cocina_insumos_bp.route('/solicitar-insumos', methods=['POST'])
@login_required
def actualiza_insumos():
    if current_user.rol_user != 3:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        data = request.get_json()
        lstSolicitudes = data.get('solicitudes')
        totalCompra = data.get('totalCompra')

        #Proceso - CompraInsumo
        objSolicitudCompra = CompraInsumo()
        objSolicitudCompra.fecha_compra = date.today().strftime('%Y-%m-%d')
        objSolicitudCompra.estatus = 0
        objSolicitudCompra.total = totalCompra
        objSolicitudCompra.id_usuario = current_user.id
        objSolicitudCompra.id_compra_insumo = dao_compra_insumo.solicitarInsumo(objSolicitudCompra)

        if objSolicitudCompra.id_compra_insumo == -1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al registrar la produccion!"
            })
        
        #Proceso - DetalleSolicitud
        for detalleSolicitud in lstSolicitudes:
            objDetalleCompra = DetalleCompraInsumo()
            objDetalleCompra.id_compra = objSolicitudCompra.id_compra_insumo
            objDetalleCompra.id_materia = detalleSolicitud["id_materia"]
            objDetalleCompra.cantidad = int(detalleSolicitud["cantidad"])
            objDetalleCompra.precio_unitario = detalleSolicitud["precio"]
            objDetalleCompra.fecha_caducidad = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
            if objDetalleCompra.cantidad == 0:  
                continue
            
            #Proceso - GuardarDetalle
            if dao_detalle_compra_insumo.agregarDetalleInsumo(objDetalleCompra) != 1:
                return jsonify({
                    "error": True,
                    "message": "Hubo un problema al registrar el detalle de insumo!"
                })

        return jsonify({
                    "success": True,
                    "message": "La solicitud se envio correctamente!"
                })

        
    except Exception as e:
        crear_log_error(current_user.usuario,'/cocina-pedidos')
        abort(404)