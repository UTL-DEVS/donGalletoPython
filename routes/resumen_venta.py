from flask import Blueprint, render_template, send_from_directory, redirect, url_for, flash
from controller import controller_resumen_venta
import os
from utils import login_required, current_user, abort

resumen_venta_bp = Blueprint('resumen_venta', __name__, template_folder='templates')

@resumen_venta_bp.route('/corte_ventas', methods=['POST'])
@login_required
def corte_ventas():
    if current_user.rol_user != 4:
        abort(404)
    try:
        filepath, error = controller_resumen_venta.corte_ventas()
        
        if error:
            flash(f'Error al generar corte: {error}', 'danger')
            return redirect(url_for('venta.tipo_venta'))
        
        filename = os.path.basename(filepath)
        
        return redirect(url_for('resumen_venta.descargar_corte', filename=filename))
        
    except Exception as e:
        flash(f'Error al generar corte: {str(e)}', 'danger')
        return redirect(url_for('venta.tipo_venta'))

@resumen_venta_bp.route('/descargar_corte/<filename>')
@login_required
def descargar_corte(filename):
    if current_user.rol_user != 4:
        abort(404)
    return send_from_directory(
        controller_resumen_venta.CORTES_FOLDER, 
        filename, 
        as_attachment=True
    )