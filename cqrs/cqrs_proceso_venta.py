class ProcesoVentaCQRS:
    @staticmethod
    def validar_item_carrito(galleta_id, cantidad, tipo_venta):
        if not galleta_id or not cantidad:
            return False, "Faltan datos requeridos"
        
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor a cero"
            
            if tipo_venta not in ['unidad', 'peso', 'paquete']:
                return False, "Tipo de venta no válido"
                
            return True, "Válido"
        except ValueError:
            return False, "Cantidad debe ser un número"