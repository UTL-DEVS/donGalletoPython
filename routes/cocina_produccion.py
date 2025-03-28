from flask import Blueprint, render_template

cocina_produccion_bp = Blueprint('cocina-produccion', __name__, template_folder='templates')

@cocina_produccion_bp.route('/working-page')
def working():
    return render_template('pages/page-produccion/working-page.html')

@cocina_produccion_bp.route('/produccion-stock')
def stock():
    return render_template('pages/page-produccion/cocina-produccion/stock.html')

@cocina_produccion_bp.route('/produccion-historial')
def historial():
    return render_template('pages/page-produccion/cocina-produccion/historial.html')