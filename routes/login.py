from utils import *
from forms import login_form
from controller import controller_login

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        captcha_data = form.captcha.data
        
        result =  controller_login(usuario, contrasenia,captcha_data)
        if result:
            return result
    return redirect('/')
        