from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Produccion(db.Model):
    __tablename__ = 'Produccion'
    id_produccion = db.Column(db.Integer, primary_key=True)
    fecha_produccion = db.Column(db.String(8), unique=True, nullable=False)
    estatus = db.Column(db.Integer, unique=True, nullable=False)

    def to_dict(self):
            return {
                "id_produccion": self.id_produccion,
                "fecha_produccion": self.fecha_produccion
            }
