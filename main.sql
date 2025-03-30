-- Active: 1742188040282@@127.0.0.1@3306@casagalleta
CREATE DATABASE casaGalleta; 
#drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;
DESCRIBE usuario;

SELECT * FROM usuario;
SELECT * FROM pre_registro;
INSERT INTO usuario(rol, email,usuario, contrasenia,token) VALUES (1,'joelbriones@gmail.com', 'adminadmin', '12345678','00');