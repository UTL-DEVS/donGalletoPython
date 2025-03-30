import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@127.0.0.1/casaGalleta' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER="tuservidor.smtp.com"
    MAIL_PORT="587"
    MAIL_USERNAME="tu_email@dominio.com"
    MAIL_PASSWORD="tu_contraseña"
    MAIL_USE_TLS="True"
    MAIL_USE_SSL="False"
    # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # # Configuración de Flask-Mail
    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = int(os.getenv('MAIL_PORT')) if os.getenv('MAIL_PORT') else None  # Conversión manual
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'False') == 'True'  # Convertir a booleano
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True') == 'True'  # Convertir a booleano