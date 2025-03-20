from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column(db.String(80), unique=True, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    
    fecha_registro = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    