from utils import *
from forms import login_form
from controller import controller_login
from funcs import hash
from datetime import datetime, timedelta
from flask import flash, redirect, url_for

login_bp = Blueprint('login', __name__, template_folder='templates')

intentos_fallidos = {}


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()
    
    if form.validate_on_submit():
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        contrasenia_hash = hash(contrasenia)
        captcha_data = form.captcha.data

        # Verificar si el usuario está bloqueado
        if usuario in intentos_fallidos:
            data = intentos_fallidos[usuario]
            if data["bloqueado"]:
                if datetime.now() < data["desbloqueo"]:
                    flash("Cuenta bloqueada temporalmente, intenta más tarde.", "danger")
                    return redirect(url_for('init_login'))
                else:
                    intentos_fallidos[usuario] = {"intentos": 0, "bloqueado": False}

        # Verificar credenciales
        result = controller_login(usuario, contrasenia_hash, captcha_data)
        if result:
            intentos_fallidos.pop(usuario, None)
            flash("Inicio de sesión exitoso", "success")
            return result

        # Si las credenciales son incorrectas
        if usuario not in intentos_fallidos:
            intentos_fallidos[usuario] = {"intentos": 0, "bloqueado": False}

        intentos_fallidos[usuario]["intentos"] += 1

        if intentos_fallidos[usuario]["intentos"] >= 5:
            intentos_fallidos[usuario]["bloqueado"] = True
            intentos_fallidos[usuario]["desbloqueo"] = datetime.now() + timedelta(minutes=5)
            flash("Cuenta bloqueada temporalmente, intenta en 5 minutos.", "danger")
            return redirect(url_for('init_login'))

        flash(f"Contraseña incorrectas. Intento {intentos_fallidos[usuario]['intentos']} de 5.", "warning")
        return redirect(url_for('init_login'))

    return redirect(url_for('init_login'))