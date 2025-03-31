from utils.db import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='completada')
    
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade="all, delete-orphan")

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tipo_venta = db.Column(db.String(20), default='unidad')
    
    galleta = db.relationship('Galleta', backref='ventas')