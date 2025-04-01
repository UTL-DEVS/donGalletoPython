from flask_mail import Message
from utils import mail

def enviar_correo(destino, cuerpo):
    msg = Message('Creacion Vuenta Casa galleta', sender='galletogalleto376@gmail.com', recipients=[destino])
    msg.body = cuerpo
    try:
        mail.send(msg)
        print('enviado')
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False