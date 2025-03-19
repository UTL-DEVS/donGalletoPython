import base64
import secrets
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from datetime import datetime, timezone
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    # cliente, admin, cocina, ventas
    rol=db.Column(db.Integer, nullable=False)
    # verificacion dos pasos
    email = db.Column(db.String(30), nullable=False)
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