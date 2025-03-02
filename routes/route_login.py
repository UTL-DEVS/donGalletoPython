from flask import render_template, Blueprint, redirect, url_for


"""
los blueprint son los links pero separados de modo que aislamos 
los links con su respectiva funcionalidad

'nombre del blueprint', 

url_for('.ruta') → Ruta dentro de la misma blueprint
url_for('nombre_ruta') → Ruta global o fuera de la blueprint
url_for('ruta', param=valor) → Arma la URL con parámetros

"""
login_bp = Blueprint('login_user', __name__, template_folder='templates')

@login_bp.route('/loginUser')
def login():
    return render_template('login/login.html')


# para poder redireccionar tambien se puede usar el nombre ya que flask lo identifica por su nombre tambien
@login_bp.route('/redi')
def redi():
    return redirect(url_for('login_user.login'))