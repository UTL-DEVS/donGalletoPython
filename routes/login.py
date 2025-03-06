from utils import *
from forms import *

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login')
def login():
    form = login_form()
    if form.validate_on_submit():
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        
        return f'Hola {usuario}, con la {contrasenia}'
    return render_template('login.html', form=form)