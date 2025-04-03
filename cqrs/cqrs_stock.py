from dao import dao_stock

def validarDatos(stock):
    if stock.id_galleta == '':
        return 'Hubo un problema al actualizar el stock, intentelo de nuevo!'
    if stock.cantidad_galleta == 0:
        return 'La cantidad no puede ser 0, intentelo de nuevo!'
    
    return ''

def agregarStock(stock):
    validacionDatos = validarDatos(stock)
    if validacionDatos != '':
        return -1
    
    return dao_stock.agregarStock(stock)  