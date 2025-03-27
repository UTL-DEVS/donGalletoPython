from utils import Blueprint, render_template

cliente_bp = Blueprint('cliente', __name__, template_folder='templates')

@cliente_bp.route('/cliente')
def index_client():
    return render_template('pages/cliente.html')


