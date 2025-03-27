from utils import *
from routes import *
from forms import *
from connection import *
from models import Usuario
from models import Galleta
def crear_app():
    app = Flask(__name__)
    app.secret_key = 'clave secreta de la app'
    
    csrf = CSRFProtect()
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(registro_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(cocina_bp)
    app.register_blueprint(cliente_bp)
    return app, csrf

app, csrf = crear_app()



#usuario = Usuario()
@app.route('/')
def init():
    form = login_form()
    if form.validate_on_submit():
        usuario=form.usuario.data
        contrasenia=form.contrasenia.data
        
    return render_template('pages/login.html', form=form)



        

if __name__ == '__main__':
    csrf.init_app(app=app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)