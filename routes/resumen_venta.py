from flask import Blueprint, render_template, send_from_directory, redirect, url_for, flash, request, abort
from controller import controller_resumen_venta
import os
from utils import login_required, current_user,abort
from funcs import crear_log_error, crear_log_user

resumen_venta_bp = Blueprint('resumen_venta', __name__, template_folder='templates')

@resumen_venta_bp.route('/corte_ventas', methods=['POST'])
@login_required
def corte_ventas():
    if current_user.rol_user != 3:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        filepath, error = controller_resumen_venta.corte_ventas()
        
        if error:
            flash(f'Error al generar corte: {error}', 'danger')
            return redirect(url_for('venta.tipo_venta'))
        
        filename = os.path.basename(filepath)
        
        return redirect(url_for('resumen_venta.descargar_corte', filename=filename))
        
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash(f'Error al generar corte: {str(e)}', 'danger')
        return redirect(url_for('venta.tipo_venta'))

@resumen_venta_bp.route('/descargar_corte/<filename>')
@login_required
def descargar_corte(filename):
    if current_user.rol_user != 3:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        return send_from_directory(
            controller_resumen_venta.CORTES_FOLDER, 
            filename, 
            as_attachment=True
        )
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("❌ Error inesperado al descargar el corte", "danger")
        return redirect('/error')