from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from datetime import datetime, timezone
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    # cliente, admin, cocina, ventas
    rol=db.Column(db.String(10), nullable=False)
    # verificacion dos pasos
    email = db.Column(db.String(30), nullable=False)
    token = db.Column(db.String(64), nullable=False)
    ultima_actividad = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)
    
    