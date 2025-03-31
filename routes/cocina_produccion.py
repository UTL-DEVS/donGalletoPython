from flask import Blueprint, render_template, request
from dao import dao_galleta, dao_detalle_produccion
from forms import DetalleRecetaForm
from datetime import date

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
def working():
    return render_template('pages/page-produccion/working-page.html')

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