import unittest
from flask import url_for
from funcs import hash
from main import app, db
from models import Usuario

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        """ Configurar entorno de prueba """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
        app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para pruebas
        self.client = app.test_client()

        with app.app_context():
            db.create_all()  # Crear tablas en la base de datos de prueba

            # Crear usuario de prueba
            self.usuario_prueba = Usuario(
                usuario="testuser",
                email="test@example.com",
                contrasenia=hash("testpassword"),
                rol_user=1,  
                token="testtoken"
            )
            db.session.add(self.usuario_prueba)
            db.session.commit()

    def tearDown(self):
        """ Limpiar la base de datos después de cada test """
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Eliminar todas las tablas

    def test_login_exitoso(self):
        """ Verifica que el usuario puede iniciar sesión con credenciales correctas """
        response = self.client.post('/login', data={
            'usuario': 'testuser',
            'contrasenia': 'testpassword',
            'captcha': '12345'  # Simulando un CAPTCHA válido
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenido', response.data)  # Ajusta según el mensaje que uses en tu template

    def test_login_fallido(self):
        """ Verifica que un usuario con contraseña incorrecta no pueda iniciar sesión """
        response = self.client.post('/login', data={
            'usuario': 'testuser',
            'contrasenia': 'wrongpassword',
            'captcha': '12345'
        })

        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Credenciales incorrectas', response.data)

    def test_login_bloqueo_por_intentos_fallidos(self):
        """ Verifica que un usuario sea bloqueado tras 5 intentos fallidos """
        for _ in range(5):
            self.client.post('/login', data={
                'usuario': 'testuser',
                'contrasenia': 'wrongpassword',
                'captcha': '12345'
            })

        response = self.client.post('/login', data={
            'usuario': 'testuser',
            'contrasenia': 'wrongpassword',
            'captcha': '12345'
        })

        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Cuenta bloqueada temporalmente, intenta en 5 minutos.', response.data)

if __name__ == '__main__':
    unittest.main()
