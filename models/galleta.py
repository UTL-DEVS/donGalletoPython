from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from datetime import datetime, timezone

class Galleta(db.Model):
    __tablename__ = 'galleta'
    id_galleta = db.Column(db.Integer, primary_key=True)
    nombre_galleta = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    precio_galleta = db.Column(db.Float, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False)
    estatus = db.Column(db.Integer, nullable=False, server_default='1')
