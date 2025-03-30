from connection.config import db
from utils.db import db

class Galleta(db.Model):
    __tablename__ = 'galletas'

    id_galleta = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    galleta = db.Column(db.String(100), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    existencia = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
