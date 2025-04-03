from flask import Blueprint, render_template, request
from utils import login_required, current_user, redirect
from dao import dao_galleta, dao_detalle_produccion
from forms import DetalleRecetaForm
from datetime import date
from utils import abort, login_required, current_user
from funcs import crear_log_error, crear_log_user

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
@login_required
def working():
    if current_user.rol_user != 0 :
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)
        return render_template('pages/page-produccion/working-page.html')
    except Exception as e:
        crear_log_error(current_user, str(e))
        return redirect('/error')

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