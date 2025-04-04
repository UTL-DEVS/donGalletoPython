-- Active: 1742188040282@@127.0.0.1@3306@casagalleta
CREATE DATABASE casaGalleta; 
drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;


SELECT * FROM usuario;
SELECT * FROM pre_registro;

use casaGalleta;
select * from galletas;
select * from stock;


Select * from pedidos;
SELECT * FROM detalles_pedido;

SELECT * FROM usuario;

DESCRIBE galletas;
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (0,'joelbriones701@gmail.com', 'joel123456', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (1,'joelbriones70@gmail.com', 'joel1234567', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (4, 'miltoner4lfredo@gmail.com', 'milk220010', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5', '00');
-- !SEGUIR ESTE ORDEN DE USUARIOS SEGUN EL ROL ESA CONTRASENIA EN EL INPUT ES: Joel123456$
-- en caso de que no los deje pasar, entonces me equivoque de formato, pero eso es la contrasenia encriptada, 
-- si no se puede crear el usuario y la contrasenia que quieran pues la ponen y ya
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (1,'cristianJoto@gmail.com', 'cristianJoto', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (0,'joelbriones@gmail.com', 'joel1234567', 'Joel123456$','00');



use casaGalleta;
INSERT INTO galletas (id_galleta, nombre_galleta, precio_galleta, imagen_galleta, descripcion_galleta, fecha_creacion, activo) 
VALUES 
(1, 'Chocolate Chip', 2.50, 'imagen1.jpg', 'Galleta con chispas de chocolate', 100, NOW(), TRUE),
(2, 'Oatmeal Raisin', 2.00, 'imagen2.jpg', 'Galleta de avena con pasas', 50, NOW(), TRUE),
(3, 'Peanut Butter', 2.75, 'imagen3.jpg', 'Galleta de mantequilla de maní', 75, NOW(), TRUE);
INSERT INTO galletas (id_galleta, nombre_galleta, precio_galleta, imagen_galleta, descripcion_galleta, cantidad_galleta, fecha_creacion, activo) 
VALUES 
(4, 'Macadamia Blanca', 3.00, 'imagen4.jpg', 'Galleta con trozos de macadamia y chocolate blanco', 60, NOW(), TRUE),
(5, 'Doble Chocolate', 2.80, 'imagen5.jpg', 'Galleta de chocolate con chispas de chocolate oscuro', 90, NOW(), TRUE),
(6, 'Red Velvet', 3.25, 'imagen6.jpg', 'Galleta estilo red velvet con crema de queso', 50, NOW(), TRUE);

(1, 'Chocolate Chip', 2.50, 'imagen1.jpg', 'Galleta con chispas de chocolate', NOW(), TRUE),
(2, 'Oatmeal Raisin', 2.00, 'imagen2.jpg', 'Galleta de avena con pasas', NOW(), TRUE),
(3, 'Peanut Butter', 2.75, 'imagen3.jpg', 'Galleta de mantequilla de maní', NOW(), TRUE);

INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, unidad_medida_publico, precio, estatus) 
VALUES ('Harina', 100.0, 1,4, 5.75, 1);

INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('SAL', 100.0, 1, 5.75, 1);
INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('pp', 100.0, 1, 5.75, 1);
INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('cc', 100.0, 1, 5.75, 1);
INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('rc', 100.0, 1, 5.75, 1);
INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('cc', 100.0, 1, 5.75, 1);
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

-- Insertar en la tabla Persona primero
INSERT INTO Persona (nombre, primerApellido, segundoApellido, correo, direccion, telefono, estatus) 
VALUES ('Juan', 'Pérez', 'Gómez', 'juan.perez@email.com', 'Calle Falsa 123, CDMX', '5551234567', 1);

-- Obtener el ID de la persona insertada
SET @id_persona = LAST_INSERT_ID();

-- Insertar en la tabla Proveedor con la persona asociada
INSERT INTO Proveedor (nombre_proveedor, id_persona) 
VALUES ('Distribuidora López', @id_persona);

SELECT * FROM proveedor;
show TABLES;
SELECT * FROM detalleReceta;
SELECT * FROM materia_prima;
SELECT * FROM persona;
SELECT * FROM receta;
show tables;
use casaGalleta;

INSERT INTO galletas (nombre_galleta, precio_galleta, imagen_galleta, descripcion_galleta, fecha_creacion, activo)
VALUES 
('Galleta de Chocolate', 2.50, 'imagen_chocolate.jpg', 'Deliciosa galleta con trozos de chocolate negro', '2023-11-15 10:30:00', true),
('Galleta de Vainilla', 2.00, 'imagen_vainilla.jpg', 'Suave galleta de vainilla con glaseado', '2023-11-15 10:30:00', true),
('Galleta de Avena', 1.80, 'imagen_avena.jpg', 'Galleta saludable con avena y pasas', '2023-11-15 10:30:00', true),
('Galleta de Mantequilla', 2.20, NULL, 'Clásica galleta de mantequilla crujiente', '2023-11-15 10:30:00', true),
('Galleta de Limón', 2.30, 'imagen_limon.jpg', 'Galleta refrescante con ralladura de limón', '2023-11-15 10:30:00', true);

INSERT INTO stock (id_galleta, cantidad_galleta, maximo_galleta, minimo_galleta) 
VALUES (4, 1000, 1400, 700);

select * from proceso_ventas;
