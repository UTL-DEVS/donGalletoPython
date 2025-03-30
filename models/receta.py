#from connection.config import db
from utils.db import db

class Receta(db.Model):
    __tablename__ = 'receta'

    id = db.Column(db.Integer, primary_key=True)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    insumos = db.relationship('RecetaInsumo', backref='receta', lazy=True)
