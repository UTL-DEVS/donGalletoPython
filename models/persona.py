from utils.db import db

class Persona(db.Model):
    __tablename__ = 'Persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=True)
    primerApellido = db.Column(db.String(80), nullable=True)
    segundoApellido = db.Column(db.String(80), nullable=True)
    correo = db.Column(db.String(30), nullable=True)
    direccion = db.Column(db.String(80), nullable=True)
    telefono = db.Column(db.String(15),nullable=True)
    estatus = db.Column(db.Integer, nullable=False, default=1)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    
    usuarios = db.relationship('Usuario', backref='persona', lazy=True)
