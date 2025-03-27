CREATE DATABASE casaGalleta;
#drop DATABASE casaGalleta;
use casaGalleta;
SHOW TABLES;
DESCRIBE usuario;

SELECT * FROM usuario;
INSERT INTO usuario(rol, email,usuario, contrasenia,token) VALUES (1,'joelbriones@gmail.com', 'adminadmin', '12345678','00');

INSERT INTO galleta (nombre_galleta, descripcion, precio_galleta, stock_minimo, stock_maximo, estatus) 
VALUES 
('Choco Chips', 'Deliciosas galletas con chispas de chocolate', 20.00, 10, 100, 1),
('Avena y Miel', 'Galletas saludables con avena y miel', 18.00, 10, 80, 1),
('Mantequilla Clásica', 'Galletas tradicionales de mantequilla', 15.00, 5, 60, 1),
('Red Velvet', 'Galletas suaves con chocolate y queso crema', 22.50, 8, 90, 1),
('Nuez Caramelizada', 'Galletas con trozos de nuez y caramelo', 25.00, 7, 70, 1),
('Triple Chocolate', 'Galletas con chocolate negro, blanco y con leche', 30.00, 10, 50, 1);

SELECT * FROM galleta;