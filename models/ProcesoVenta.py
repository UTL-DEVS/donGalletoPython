from utils.db import db
from datetime import datetime

class ProcesoVenta(db.Model):
    __tablename__ = 'proceso_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    estado = db.Column(db.String(20), default='completada', nullable=False)
    
    detalles = db.relationship('DetalleVenta', back_populates='proceso_venta', cascade="all, delete-orphan")

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('proceso_ventas.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tipo_venta = db.Column(db.String(20), default='unidad', nullable=False)
    
    galleta = db.relationship('Galleta', back_populates='detalles_venta')
    proceso_venta = db.relationship('ProcesoVenta', back_populates='detalles')