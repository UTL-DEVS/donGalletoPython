from cqrs import  cqrs_registro

def controller_registro(email, usuario, contrasenia, captcha):
    return cqrs_registro(email, usuario, contrasenia, captcha)
    