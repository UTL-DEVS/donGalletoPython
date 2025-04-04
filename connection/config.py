import os
#from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
#load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1/casaGalleta'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT='465'
    MAIL_USERNAME='galletogalleto376@gmail.com'
    MAIL_PASSWORD='wtqzaoucynorezrl'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True

