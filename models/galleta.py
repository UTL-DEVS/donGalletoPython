from utils.db import db
from datetime import datetime

class Galleta(db.Model):
    __tablename__ = 'galletas'
    id_galleta = db.Column(db.Integer, primary_key=True)
    nombre_galleta = db.Column(db.String(100), nullable=False)
    precio_galleta = db.Column(db.Float, nullable=False)
    imagen_galleta = db.Column(db.Text, nullable=True)
    descripcion_galleta = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    escogido = db.Column(db.Boolean, default=True)
    

    stock = db.relationship('Stock', back_populates='galleta', uselist=False)
    detalles_venta = db.relationship('DetalleVenta', back_populates='galleta')

    def __repr__(self):
        return f'<Galleta {self.nombre_galleta}>'