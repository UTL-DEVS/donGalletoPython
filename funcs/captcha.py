# this module is to use the generation of captcha

from captcha.image import ImageCaptcha
from utils import session
import io
import base64
import random
from datetime import datetime, timedelta # timedelta is the unit time for example months, days, seconds ...
import os

def captcha_info():
    numero = random.randrange(11111, 99999)
    captcha_txt = str(numero)
    session['captcha_txt'] = captcha_txt  # Guardamos el texto del CAPTCHA en la sesión
    captcha_time = datetime.now()
    session['captcha_time'] = captcha_time
    
    # Crear la imagen del CAPTCHA
    imagen = ImageCaptcha(width=200, height=70)
    captcha_image = imagen.generate_image(captcha_txt)

    # Convertir la imagen a formato Base64
    img_io = io.BytesIO()
    captcha_image.save(img_io, 'PNG')
    img_io.seek(0)
    captcha_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return captcha_base64

def delate_captcha_session(captcha):
    session.pop(f'{captcha}', None)
    

def verificar_captcha():
    captcha_txt = session.get('captcha_txt')
    captcha_time = session.get('captcha_time')
    
    if captcha_time.tzinfo is not None:
        captcha_time = captcha_time.replace(tzinfo=None)  # Convertirlo a naive (sin zona horaria)

    actual = datetime.now()


    captcha_time_minute = captcha_time.replace(second=0, microsecond=0)
    actual_minute = actual.replace(second=0, microsecond=0)


    dato = actual_minute - captcha_time_minute
    return dato.total_seconds(), captcha_txt