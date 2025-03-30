from connection.config import db
from utils.db import db

class RecetaInsumo(db.Model):
    __tablename__ = 'receta_insumo'

    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id_insumo'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
