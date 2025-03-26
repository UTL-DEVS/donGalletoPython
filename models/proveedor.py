from flask_sqlalchemy import SQLAlchemy
from utils.db import db

class Proveedor(db.Model):
    __tablename__ = 'Proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column(db.String(80), unique=True, nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('Persona.id_persona'), nullable=False)  # Persona 
    
    persona = db.relationship('Persona', backref=db.backref('Proveedor', uselist=False))

    def to_dict(self):
            return {
                "id_proveedor": self.id_proveedor,
                "nombre": self.nombre_proveedor,
                "representante": f'{self.persona.nombre} {self.persona.primerApellido} {self.persona.segundoApellido}',
                "correo": self.persona.correo,
                "telefono": self.persona.telefono,
                "direccion": self.persona.direccion
            }