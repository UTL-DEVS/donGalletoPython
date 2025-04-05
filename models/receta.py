from utils.db import db
class Receta(db.Model):
    
    __tablename__ = 'receta'
    id_receta = db.Column(db.Integer, primary_key=True)
    id_galleta = db.Column(db.Integer, db.ForeignKey('galletas.id_galleta'), nullable=False)
    nombre_receta = db.Column(db.String(100), nullable=False, unique=True)
    estado = db.Column(db.String(1), nullable=False)
    cantidad_insumo_producida = db.Column(db.Integer, nullable=False)
