from utils.db import db

class Empleado(db.Model):
    __tablename__ = 'Empleado'
    id_empleado = db.Column(db.Integer, primary_key=True)
    sueldo_empleado = db.Column(db.Float, nullable=False, default=1.0)
    dias_laborales = db.Column(db.Integer, nullable=False, default=1)
    id_persona = db.Column(db.Integer, db.ForeignKey('Persona.id_persona'), nullable=False)  # Persona 
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Usuario 
    
    persona = db.relationship('Persona', backref=db.backref('Empleado', uselist=False))
    usuario = db.relationship('Usuario', backref=db.backref('Empleado', uselist=False))

    def to_dict(self):
            return {
                "id_empleado": self.id_empleado,
                "sueldo_empleado": self.sueldo_empleado,
                "dias_laborales": self.dias_laborales
            }