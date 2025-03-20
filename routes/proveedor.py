from flask import Blueprint, render_template

proveedor_bp = Blueprint('proveedor', __name__, template_folder='templates')

@proveedor_bp.route('/proveedor')
def proveedor():
    return render_template('pages/proveedor.html')