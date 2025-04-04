from utils.db import db

class Nomina(db.Model):
    __tablename__ = 'Nomina'
    id_nomina = db.Column(db.Integer, primary_key=True)
    cantidad_pagada = db.Column(db.Float, nullable=False, default=1.0)
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=False)
    
    estatus = db.Column(db.Integer, nullable=False, default=1)
    fecha_pago = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    
    empleado = db.relationship('Empleado', backref='nomina', lazy=True)
