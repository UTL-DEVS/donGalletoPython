from utils.db import db

class Galleta(db.Model):
    __tablename__ = 'Galleta'
    
    id_galleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_galleta = db.Column(db.String(50), nullable=False)
    precio_galleta = db.Column(db.Float, nullable=False)
    imagen_galleta = db.Column(db.Text, nullable=True)
    descripcion = db.Column(db.String(100), nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False)
    estatus = db.Column(db.Integer, nullable=False)


    
