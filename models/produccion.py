from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Produccion(db.Model):
    __tablename__ = 'produccion'
    id_produccion = db.Column(db.Integer, primary_key=True)
    fecha_produccion = db.Column(db.String(10), nullable=False)
    hora_produccion = db.Column(db.String(10), nullable=False)
    estatus = db.Column(db.Integer, nullable=False)

    def to_dict(self):
            return {
                "id_produccion": self.id_produccion,
                "fecha_produccion": self.fecha_produccion
            }
