from utils.db import db

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'
    
    id_materia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_materia = db.Column(db.String(100), nullable=False)
    stock_materia = db.Column(db.Float, nullable=False)
    unidad_medida = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.Integer, nullable=False, default=1)

