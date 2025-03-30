#from connection.config import db
from utils.db import db

class Insumo(db.Model):
    __tablename__ = 'insumos'

    id_insumo = db.Column(db.Integer, primary_key=True)
    nombreInsumo = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.id_proveedor'), nullable=False)
    proveedor = db.relationship('Proveedor', backref=db.backref('Insumos', uselist=False))
