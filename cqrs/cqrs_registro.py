from dao import dao_registro, dao_conf

def cqrs_registro(*args):
    for elemento in args:
        elemento = str(elemento)
        if elemento.strip() == '' or elemento is None:
            return False
    email = args[0]
    usuario = args[1]
    contrasenia = args[2]
    captcha = args[3]
    result = dao_registro(email, usuario, contrasenia, captcha)
    return result

def cqrs_conf(*args):
    for elemnto in args:
        for elemento in args:
            elemento = str(elemento)
        if elemento.strip() == '' or elemento is None:
            return False
    email = args[0]
    token = args[1]
    result = dao_conf(email, token)
    return result
    