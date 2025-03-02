from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from routes.route_login import login_bp

from connection.config import Config

db = SQLAlchemy()

# el blue a registrar, y el prefijo por el que aparece, login/login_user

def crearApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    #Esta línea carga la configuración de la aplicación Flask desde una clase (en este caso Config)
    app.register_blueprint(login_bp, url_prefix='/login')
    # crear el contexto de la app y meterlo al hilo actual
    app.app_context().push()
    try:
        # corroboral la coneccion
        db.engine.connect()
        print("Conectado a la base de datos")
    except Exception as e:
        print("Error al conectar a la base de datos: ", e)
    return app

app = crearApp()

@app.route('/')
def main():
    return render_template('login/login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)

