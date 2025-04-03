from flask import Blueprint, render_template, request, jsonify
from datetime import date, datetime
from forms import DetalleRecetaForm
from flask import Blueprint, render_template, request
from models.materiaPrima import MateriaPrima
from controller import controller_materia_prima
from dao import dao_insumos
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
        if controller_materia_prima.actualizarStock(lstSolicitudes) != 1:
            return jsonify({
                "error": True,
                "message": "Hubo un problema al solicitar el Stock!"
            })
        
        return jsonify({
                "success": True,
                "message": "La solicitud se agrego correctamente al Stock!"
            })
        
    except Exception as e:
        crear_log_error(current_user.usuario,'/cocina-pedidos')
        abort(404)