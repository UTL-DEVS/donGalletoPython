def validar_producto(data):
    if not data.get('nombre') or not data.get('precio'):
        return False
    try:
        precio = float(data['precio'])
        if precio <= 0:
            return False
    except ValueError:
        return False
    return True