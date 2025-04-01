from utils import Blueprint, render_template, redirect, flash
from forms import regis_form, conf_form
from funcs import captcha_info
from controller import controller_registro, controller_conf

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
        if resultado is False:
            return redirect('/registro')
        else:
            return redirect('/confirmar')
    captcha_data = captcha_info()
    return render_template('pages/registro.html', form=form, captcha_base64=captcha_data)

@registro_bp.route('/confirmar', methods=['POST', 'GET'])
def conf_registro():
    form = conf_form()
    if form.validate_on_submit():
        email = form.email.data
        token = form.token.data
        if controller_conf(email=email, token=token):
            return redirect('/cliente')
        else:
            return redirect('/login')
    return render_template('pages/confirmar.html', form=form)