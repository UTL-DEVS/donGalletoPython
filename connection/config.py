from flask_sqlalchemy import SQLAlchemy

class Config():
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:contraseña@localhost/nombre_de_base_de_datos'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    try:
        
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/galletoprueba'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    except Exception as e:
        print(f'el error es : {e}')