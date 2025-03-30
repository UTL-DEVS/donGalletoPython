def validar_item_carrito(data):
    if not data.get('galleta_id') or not data.get('cantidad'):
        return False
    try:
        cantidad = int(data['cantidad'])
        if cantidad <= 0:
            return False
    except ValueError:
        return False
    return True