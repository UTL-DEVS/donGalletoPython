from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class DetalleProduccion(db.Model):
    __tablename__ = 'detalle_produccion'
    id_detalle_produccion = db.Column(db.Integer, primary_key=True)
    id_galleta = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    id_produccion = db.Column(db.Integer, db.ForeignKey('produccion.id_produccion'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    
    galleta = db.relationship('Galleta', backref=db.backref('DetalleProduccion', uselist=False))
    produccion = db.relationship('Produccion', backref=db.backref('DetalleProduccion', uselist=False))

    def to_dict(self):
            return {
                "id_detalle_produccion": self.id_detalle_produccion,
                "id_galleta": self.galleta.id_galleta,
                "id_produccion": self.produccion.id_produccion,
                "cantidad": self.cantidad
            }
