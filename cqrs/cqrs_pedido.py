from dao.dao_cliente import dao_cliente

def validarDatos(pedido):
    if pedido.id_pedido == '':
        return 'Hubo un problema al actualizar el pedido, intentelo de nuevo!'

    return ''

def actualizarPedido(idPedido):
    return dao_cliente.actualizarEstatusPedido(idPedido)
