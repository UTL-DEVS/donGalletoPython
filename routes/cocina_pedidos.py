from flask import Blueprint, render_template

cocina_pedidos_bp = Blueprint('cocina-pedidos', __name__, template_folder='templates')

@cocina_pedidos_bp.route('/cocina-pedidos')
def cocina_pedidos():
    return render_template('pages/page-produccion/cocina-pedidos/pedidos.html')