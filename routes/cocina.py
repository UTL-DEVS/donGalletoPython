from flask import Blueprint, render_template

cocina_bp = Blueprint('cocina', __name__, template_folder='templates')

@cocina_bp.route('/cocina')
def cocina():
    return render_template('pages/page-cocina/cocina.html')