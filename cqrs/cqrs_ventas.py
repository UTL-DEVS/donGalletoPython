def validar_galleta(data):
    if not data.get('nombre_galleta') or not data.get('precio_galleta'):
        return False
    try:
        precio = float(data['precio_galleta'])
        if precio <= 0:
            return False
    except ValueError:
        return False
    return True