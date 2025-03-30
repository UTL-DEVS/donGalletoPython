from cqrs import  cqrs_registro,  cqrs_conf

def controller_registro(email, usuario, contrasenia, captcha):
    return cqrs_registro(email, usuario, contrasenia, captcha)

def controller_conf(email, token):
    return cqrs_conf(email, token)