CREATE DATABASE casaGalleta; 
#drop DATABASE casaGalleta;

use casaGalleta;
SHOW TABLES;
DESCRIBE usuario;

SELECT * FROM usuario;
INSERT INTO usuario(rol, email,usuario, contrasenia,token) VALUES (1,'joelbriones@gmail.com', 'adminadmin', '12345678','00');