from utils import *
from routes import *
from forms import *
from connection import *
from models import *
from controller import *
from funcs import crear_log_error, crear_log_user
import unittest
from flask_login import current_user

import hashlib
import random
import base64
import io
import os
from datetime import timedelta
from funcs import captcha_info
from flask import Flask, session
from flask_session import Session

# comando a ejecutar en terminal


def crear_app():
    app = Flask(__name__)
    app.secret_key = 'clave secreta de la app'
    
    csrf = CSRFProtect()
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    
    app.register_blueprint(registro_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(cocina_produccion_bp)
    app.register_blueprint(cocina_pedidos_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(economia_bp)
    app.register_blueprint(recetas_bp)
    app.register_blueprint(galleta_bp)
    app.register_blueprint(resumen_venta_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(route_galleta)
    app.register_blueprint(insumos_bp)
    app.register_blueprint(cocina_insumos_bp)
    app.register_blueprint(venta_bp)

    return app, csrf

app, csrf = crear_app()


login_manager = LoginManager()
login_manager.login_view = "login.login"
login_manager.init_app(app)

# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False
Session(app)



@app.route('/home')
def init():
        galletas = ClienteController.obtener_galletas_activas()
        return render_template('index.html', galletas=galletas)

@app.route('/')
def init_login():
    form = login_form()  
    captcha_base64 = captcha_info()
    
    # Renderizar la plantilla con la imagen en Base64
    return render_template('pages/login.html', form=form, captcha_base64=captcha_base64)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id)) 

@app.route('/logout')
def logout():
    
    
    logout_user()
    return redirect(url_for('login.login'))

@app.errorhandler(404)
def page_not_found(e):
    # Obtener la IP del usuario
    ip_usuario = request.remote_addr

    # Verificar si el usuario está autenticado antes de acceder a sus atributos
    usuario = current_user.usuario if current_user.is_authenticated else "Usuario anónimo"
    
    # Registrar el error con la IP
    crear_log_error(usuario, f"Error 404: Página no encontrada en {request.url} | IP: {ip_usuario}")
    
    # Si el usuario está autenticado, cerramos su sesión
    if current_user.is_authenticated:
        logout_user()
    
    return render_template('pages/error.html'), 404

@app.cli.command()
def test():
    test=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(test)
        

if __name__ == '__main__':
    csrf.init_app(app=app)
    with app.app_context():
        db.create_all()
    app.run( port=8080, debug=True)