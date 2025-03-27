class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/casaGalleta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'galletogalleto376@gmail.com'
    MAIL_PASSWORD = 'ippdhvsykegokzcj'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
