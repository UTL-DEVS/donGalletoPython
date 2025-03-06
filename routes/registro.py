from flask import Blueprint, render_template

registro_bp = Blueprint('registro', __name__, template_folder='templates')

@registro_bp.route('/registro')
def registro():
    return render_template('pages/registro.html')