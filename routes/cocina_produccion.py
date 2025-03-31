from flask import Blueprint, render_template, request
from utils import login_required, current_user, redirect
from dao import dao_galleta, dao_detalle_produccion
from forms import DetalleRecetaForm
from datetime import date

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
@login_required
def working():
    if current_user.rol_user != 0:
        return redirect('/')
    return render_template('pages/page-produccion/working-page.html')

@cocina_produccion_bp.route('/produccion-stock')
@login_required
def stock():
    if current_user.rol_user != 0:
        return redirect('/')
    form = DetalleRecetaForm()
    lstGalletas = dao_galleta.getAllGalletas()
    return render_template('pages/page-produccion/cocina-produccion/stock.html', lstGalletas = lstGalletas, form = form)

@cocina_produccion_bp.route('/produccion-historial', methods=['GET'])
@login_required
def historial():
    if current_user.rol_user != 0:
        return redirect('/')
    fecha = request.args.get('fecha')
    if fecha == None:
        fecha = date.today().strftime('%Y-%m-%d')
    lstGalletas = dao_detalle_produccion.obtenerDetalleProduccion(fecha)
    return render_template('pages/page-produccion/cocina-produccion/historial.html', lstGalletas = lstGalletas, fecha = fecha)