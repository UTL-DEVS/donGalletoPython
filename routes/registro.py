from utils import Blueprint, render_template, redirect
from forms import regis_form
from funcs import captcha_info
from controller import controller_registro

registro_bp = Blueprint('registro', __name__, template_folder='templates')

@registro_bp.route('/registro', methods=['POST', 'GET'])
def registro():
    form = regis_form()
    if form.validate_on_submit():
        email = form.email.data
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        captcha = form.captcha.data
        resultado = controller_registro(email, usuario, contrasenia, captcha)
        return 'hola'
    captcha_data = captcha_info()
    return render_template('pages/registro.html', form=form, captcha_base64=captcha_data)