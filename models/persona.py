from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Persona(db.Model):
    __tablename__ = 'Persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    primerApellido = db.Column(db.String(80), nullable=False)
    segundoApellido = db.Column(db.String(80))
    correo = db.Column(db.String(30))
    direccion = db.Column(db.String(80))
    telefono = db.Column(db.String(15))
    
    fecha_registro = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    