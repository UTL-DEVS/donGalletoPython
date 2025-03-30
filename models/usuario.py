import base64
import secrets
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from datetime import datetime, timezone, timedelta
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    # cliente, admin, cocina, ventas
    rol_user=db.Column(db.Integer, nullable=False)
    # verificacion dos pasos
    email = db.Column(db.String(100), nullable=False,unique=True)
    token = db.Column(db.Text, nullable=False)
    
    ultimo_acceso = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)
    sistema = db.Column(db.Integer, nullable=False, server_default='0' )
    
    def generar_token(self):
        token_bytes = secrets.token_bytes(32)
        self.token = base64.b64encode(token_bytes).decode('utf-8')
        
        db.session.commit()
    def generar_ultimo_acceso(self):
        self.ultimo_acceso = datetime.now(timezone.utc)
        self.sistema = 1
        db.session.commit()
    def dentro_sistema(self):
        self.sistema = 1
        db.session.commit()
    def fuera_sistema(self):
        self.sistema = 0
        db.session.commit()
    
    @classmethod
    def validar_token(cls, token):
        usuario_local = Usuario.query.filter_by(token=token).first()
        if usuario_local and usuario_local.token != '00000000':  # Validación básica
            return usuario_local
        return None 

class PreRegistro(db.Model):
    __tablename__ = 'pre_registro'
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False,unique=True)
    token = db.Column(db.String(5), nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)
    fecha = fecha = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    
    @classmethod
    def eliminar_registros_expirados(cls):
        tiempo_limite = datetime.now(timezone.utc) - timedelta(minutes=5)
        registros_a_eliminar = cls.query.filter(cls.fecha < tiempo_limite).all()
        
        if registros_a_eliminar:
            for registro in registros_a_eliminar:
                db.session.delete(registro)
            db.session.commit()
    