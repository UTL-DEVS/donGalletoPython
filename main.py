from utils import *
from routes import *
from forms import *
from connection import *
from models import *

import hashlib
import random
import base64
import io
import os
from datetime import timedelta
from funcs import captcha_info

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
    app.register_blueprint(produccion_bp)
    app.register_blueprint(recetas_bp)
    app.register_blueprint(galleta_bp)
    app.register_blueprint(resumen_bp)
    app.register_blueprint(usuario_bp)

    
    
    return app, csrf

app, csrf = crear_app()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"



@app.route('/')
def init():
    form = login_form()  

    
    captcha_base64 = captcha_info()
    
    # Renderizar la plantilla con la imagen en Base64
    return render_template('pages/login.html', form=form, captcha_base64=captcha_base64)
        


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

        

if __name__ == '__main__':
    csrf.init_app(app=app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)