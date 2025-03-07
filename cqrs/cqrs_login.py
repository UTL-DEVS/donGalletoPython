def cqrs_login(*args):
    for elemento in args:
        elemento = str(elemento)
        if elemento.strip() == '' or elemento is None:
            return False
    return True