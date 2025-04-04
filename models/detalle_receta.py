from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class DetalleReceta(db.Model):
    __tablename__ = 'detalle_receta'
    id_detalle_receta = db.Column(db.Integer, primary_key=True)
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id_receta'), nullable=False)
    cantidad_insumo = db.Column(db.Float, nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia_prima.id_materia'), nullable=False)
    