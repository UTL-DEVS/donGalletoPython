from dao import dao_login

def cqrs_login(*args):
    usuario = args[0]
    contrasenia = args[1]
    captcha_data = args[2]
    for elemento in args:
        elemento = str(elemento)
        if elemento.strip() == '' or elemento is None:
            return False
    result = dao_login(usuario, contrasenia, captcha_data)
    return result