from utils import *
from forms import *
from controller import controller_login

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    print('Hola')
    form = login_form()
    if form.validate_on_submit():
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        respuesta = controller_login(usuario, contrasenia)
        if respuesta != None:
            return respuesta
        else:
            return 'Error al iniciar sesión'