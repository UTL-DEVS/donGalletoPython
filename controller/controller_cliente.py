from dao.dao_cliente import dao_cliente as ClienteDAO
from flask import session, flash
from cqrs import cqrs_pedido

class ClienteController:
    @staticmethod
    def obtener_galletas_activas():
        return ClienteDAO.obtener_galletas_activas()
    
    @staticmethod
    def obtener_galleta(id_galleta):
        return ClienteDAO.obtener_galleta_por_id(id_galleta)
    
    @staticmethod
    def calcular_precio(tipo_pedido, id_galleta, form_data):
        galleta = ClienteDAO.obtener_galleta_por_id(id_galleta)
        if not galleta:
            raise ValueError("Galleta no encontrada")
            
        if tipo_pedido == "paquete":
            peso = int(form_data.get('paquete', 700))
            cantidad_galleta = int(form_data.get('cantidad', 1))
            if peso == 700:
                return galleta.precio_galleta * 70 * cantidad_galleta
            else:
                return galleta.precio_galleta * 100 * cantidad_galleta
                
        elif tipo_pedido == "peso":
            peso = int(form_data.get('peso', 100))
            cantidad_galleta = int(form_data.get('cantidad', 1))
            return (galleta.precio_galleta * (peso / 10)) * cantidad_galleta
            
        elif tipo_pedido == "pieza":
            cantidad_galleta = int(form_data.get('cantidad', 1))
            return galleta.precio_galleta * cantidad_galleta
    
    @staticmethod
    def agregar_al_carrito(id_galleta, nombre, precio, cantidad_galleta, tipo_pedido,):
        if not all([id_galleta, nombre, precio, cantidad_galleta, tipo_pedido]):
            raise ValueError("Faltan datos requeridos")
            
        carrito = session.get('carrito', [])
        item_existente = next(
            (item for item in carrito 
            if item['id'] == id_galleta and item['tipo_pedido'] == tipo_pedido),
            None
        )
        
        if item_existente:
            item_existente['cantidad'] += int(cantidad_galleta)
            item_existente['precio'] = float(precio)  # Update price in case it changed
        else:
            carrito.append({
                'id': int(id_galleta),
                'nombre': str(nombre),
                'precio': float(precio),
                'cantidad': int(cantidad_galleta),
                'tipo_pedido': str(tipo_pedido)
            })
        
        session['carrito'] = carrito
        session.modified = True
        return True
    
    @staticmethod
    def eliminar_del_carrito(index):
        carrito = session.get('carrito', [])
        if 0 <= index < len(carrito):
            item = carrito.pop(index)
            session['carrito'] = carrito
            session.modified = True
            return item
        return None
    
    @staticmethod
    def realizar_pedido(id_usuario):
        carrito = session.get('carrito', [])
        if not carrito:
            raise ValueError("El carrito está vacío")
        
        pedido = ClienteDAO.crear_pedido(id_usuario, carrito)
        session.pop('carrito', None)
        return pedido
    
    @staticmethod
    def calcular_total():
        carrito = session.get('carrito', [])
        return round(sum(item["precio"] * item["cantidad"] for item in carrito), 2)
    
    @staticmethod
    def obtener_pedido(id_pedido):
        return ClienteDAO.obtener_pedido_por_id(id_pedido)
    
    @staticmethod
    def vaciar_carrito():
        if 'carrito' in session:
            session.pop('carrito')
            return True
        return False
    
    @staticmethod
    def actualizarPedido(idPedido):
        return cqrs_pedido.actualizarPedido(idPedido)