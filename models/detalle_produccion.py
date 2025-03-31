from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class DetalleProduccion(db.Model):
    __tablename__ = 'DetalleProduccion'
    id_detalle_produccion = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('Receta.id_receta'), nullable=False)
    id_produccion = db.Column(db.Integer, db.ForeignKey('Produccion.id_produccion'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    
    receta = db.relationship('Receta', backref=db.backref('DetalleProduccion', uselist=False))
    produccion = db.relationship('Produccion', backref=db.backref('DetalleProduccion', uselist=False))


    def to_dict(self):
            return {
                "id_detalle_produccion": self.id_detalle_produccion,
                "id_receta": self.receta.id_receta,
                "id_produccion": self.produccion.id_produccion,
                "cantidad": self.cantidad
            }
