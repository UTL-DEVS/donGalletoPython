from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.db import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha_pedido = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))
    estatus = db.Column(db.String(20)) # en_proceso, completado, cancelado

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'))
    id_galleta = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'))
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    tipo_pedido = db.Column(db.String(50))
    pedido = db.relationship('Pedido', backref='detalles')
    galleta = db.relationship('Galleta')
