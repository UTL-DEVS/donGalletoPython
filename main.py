from utils import *
from routes import *
from forms import *
from connection import *
from models import Usuario
import hashlib
from captcha.image import ImageCaptcha
import random
import base64
import io

def crear_app():
    app = Flask(__name__)
    app.secret_key = 'clave secreta de la app'
    
    csrf = CSRFProtect()
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(registro_bp)
    app.register_blueprint(login_bp)
    return app, csrf

app, csrf = crear_app()



#usuario = Usuario()
@app.route('/')
def init():
    form = login_form()  

    numero = random.randrange(11111, 99999)
    captcha_txt = str(numero)
    session['captcha_txt'] = captcha_txt  # Guardamos el texto del CAPTCHA en la sesión

    # Crear la imagen del CAPTCHA
    imagen = ImageCaptcha(width=200, height=70)
    captcha_image = imagen.generate_image(captcha_txt)

    # Convertir la imagen a formato Base64
    img_io = io.BytesIO()
    captcha_image.save(img_io, 'PNG')
    img_io.seek(0)
    captcha_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # Renderizar la plantilla con la imagen en Base64
    return render_template('pages/login.html', form=form, captcha_base64=captcha_base64)


        

if __name__ == '__main__':
    csrf.init_app(app=app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)