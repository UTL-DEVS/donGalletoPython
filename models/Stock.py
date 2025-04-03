from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Stock(db.Model):
    __tablename__ = 'stock'
    id_stock = db.Column(db.Integer, primary_key=True)
    id_galleta = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    cantidad_galleta = db.Column(db.Integer, nullable=False, default=0)
    maximo_galleta = db.Column(db.Integer, nullable=False, default=1400)
    minimo_galleta = db.Column(db.Integer, nullable=False, default=700)
    
    galleta = db.relationship('Galleta', backref=db.backref('detalleGalleta', uselist=False))
    galleta = db.relationship('Galleta', back_populates='stock')
    