-- Active: 1742188040282@@127.0.0.1@3306@casagalleta
CREATE DATABASE casaGalleta; 
drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;


INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (0,'joelbriones701@gmail.com', 'joel123456', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (1,'joelbriones70@gmail.com', 'joel1234567', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (4, 'miltoner4lfredo@gmail.com', 'milk220010', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5', '00');
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (3,'joelbriones470@gmail.com', 'joel12345678', 'e39ab699d50e9eacbe2abf4320192d33de6465592c8752939ec20183de8462e5','00');

-- !SEGUIR ESTE ORDEN DE USUARIOS SEGUN EL ROL ESA CONTRASENIA EN EL INPUT ES: Joel123456$
-- en caso de que no los deje pasar, entonces me equivoque de formato, pero eso es la contrasenia encriptada, 
-- si no se puede crear el usuario y la contrasenia que quieran pues la ponen y ya

select * FROM usuario;
select * FROM pre_registro;


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





-- Insertar en la tabla Persona primero
INSERT INTO Persona (nombre, primerApellido, segundoApellido, correo, direccion, telefono, estatus) 
VALUES ('Juan', 'Pérez', 'Gómez', 'juan.perez@email.com', 'Calle Falsa 123, CDMX', '5551234567', 1);

-- Obtener el ID de la persona insertada
SET @id_persona = LAST_INSERT_ID();

-- Insertar en la tabla Proveedor con la persona asociada
INSERT INTO Proveedor (nombre_proveedor, id_persona) 
VALUES ('Distribuidora López', @id_persona);


INSERT INTO `detalle_receta` (`id_detalle_receta`,`id_receta`,`cantidad_insumo`,`id_materia`) VALUES (1,1,10,1);
INSERT INTO `galletas` (`id_galleta`,`nombre_galleta`,`precio_galleta`,`imagen_galleta`,`descripcion_galleta`,`fecha_creacion`,`activo`) VALUES (1,'Chocolate Chip',2.5,'imagen1.jpg','Galleta con chispas de chocolate','2025-04-03 18:44:14',1);
INSERT INTO `galletas` (`id_galleta`,`nombre_galleta`,`precio_galleta`,`imagen_galleta`,`descripcion_galleta`,`fecha_creacion`,`activo`) VALUES (2,'Oatmeal Raisin',2,'imagen2.jpg','Galleta de avena con pasas','2025-04-03 18:44:14',1);
INSERT INTO `galletas` (`id_galleta`,`nombre_galleta`,`precio_galleta`,`imagen_galleta`,`descripcion_galleta`,`fecha_creacion`,`activo`) VALUES (3,'Peanut Butter',2.75,'imagen3.jpg','Galleta de mantequilla de maní','2025-04-03 18:44:14',1);
INSERT INTO `Proveedor` (`id_proveedor`,`nombre_proveedor`,`id_persona`) VALUES (1,'Maseca',1);
INSERT INTO `receta` (`id_receta`,`id_galleta`,`nombre_receta`,`estado`) VALUES (1,1,'Chocolate Chip','1');
INSERT INTO `stock` (`id_stock`,`id_galleta`,`cantidad_galleta`,`maximo_galleta`,`minimo_galleta`) VALUES (1,1,1,50,10);

INSERT INTO materia_prima (id_materia,nombre_materia,stock_materia,unidad_medida_publico,unidad_medida,precio,estatus,id_proveedor) VALUES (1,'Harina',147,1,1,50,1,1);

SELECT * FROM galletas;
SELECT * FROM detalle_receta;


SELECT * from materia_prima;