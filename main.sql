CREATE DATABASE casaGalleta; 
drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;

SELECT * FROM usuario;
SELECT * FROM pre_registro;

select * from galletas;

DESCRIBE galletas;
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (0,'joelbriones@   gmail.com', 'joel123456', 'Joel123456$','00');



INSERT INTO galletas (id_galleta, nombre_galleta, precio_galleta, imagen_galleta, descripcion_galleta, cantidad_galleta, fecha_creacion, activo) 
VALUES 
(1, 'Chocolate Chip', 2.50, 'imagen1.jpg', 'Galleta con chispas de chocolate', 100, NOW(), TRUE),
(2, 'Oatmeal Raisin', 2.00, 'imagen2.jpg', 'Galleta de avena con pasas', 50, NOW(), TRUE),
(3, 'Peanut Butter', 2.75, 'imagen3.jpg', 'Galleta de mantequilla de maní', 75, NOW(), TRUE);

INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('Harina', 100.0, 1, 5.75, 1);

INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('SAL', 100.0, 1, 5.75, 1);
/*
 __tablename__ = 'galletas'
    id_galleta = db.Column(db.Integer, primary_key=True)
    nombre_galleta = db.Column(db.String(100), nullable=False)
    precio_galleta = db.Column(db.Float, nullable=False)
    imagen_galleta = db.Column(db.Text, nullable=True)
    descripcion_galleta = db.Column(db.Text, nullable=True)
    cantidad_galleta = db.Column(db.Integer, default=0, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

*/




INSERT INTO Receta (nombre_receta, estado) 
VALUES ('Receta galleta Chocolate', '1');

INSERT INTO detalle_receta (cantidad_insumo, id_galleta, id_materia, receta_id) 
VALUES (2.5, 1, 1,1); 

use casaGalleta;
SELECT * FROM detalle_receta;