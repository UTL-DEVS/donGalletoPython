from cqrs import cqrs_login
from dao import dao_login
import os

def controller_login(usuario, contrasenia, captcha_data):
    
    
    
    return cqrs_login(usuario, contrasenia, captcha_data)