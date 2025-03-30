from dao import dao_login

def cqrs_login(*args):
    for elemento in args:
        elemento = str(elemento)
        if elemento.strip() == '' or elemento is None:
            return False
    usuario = args[0]
    contrasenia = args[1]
    captcha_data = args[2]
    result = dao_login(usuario, contrasenia, captcha_data)
    return result