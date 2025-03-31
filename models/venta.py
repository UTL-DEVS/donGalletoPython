from utils.db import db
from datetime import datetime, timedelta

class Venta(db.Model):
    __tablename__ = 'Venta'
    
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False, default=datetime.now().date)
    total_venta = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.Integer, nullable=False, default=1)
    
    # Relación con DetalleVenta
    detalles = db.relationship('DetalleVenta', backref='venta', cascade='all, delete-orphan', lazy=True)
    
