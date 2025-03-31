CREATE DATABASE casaGalleta; 
#drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;

SELECT * FROM usuario;
SELECT * FROM pre_registro;
INSERT INTO usuario(rol_user, email,usuario, contrasenia,token) VALUES (1,'joelbriones@gmail.com', 'adminadmin', '12345678','00');

INSERT INTO Galleta (nombre_galleta, precio_galleta, stock_minimo, stock_maximo, estatus) 
VALUES ('ChocoChip', 10.50, 50, 200, 1);

INSERT INTO materia_prima (nombre_materia, stock_materia, unidad_medida, precio, estatus) 
VALUES ('Harina', 100.0, 1, 5.75, 1);

INSERT INTO Receta (nombre_receta, estado) 
VALUES ('Receta galleta Chocolate', '1');

INSERT INTO detalle_receta (cantidad_insumo, id_galleta, id_materia, receta_id) 
VALUES (2.5, 1, 1,1); 

SELECT * FROM detalle_receta;