from dao import dao_economia

def obtener_ventas_diarias(mes, dias):
    return dao_economia.obtener_ventas_por_mes(mes, dias)

def obtener_fechas_ventas():
        fechas_ventas = '{"primera_venta": "'+dao_economia.obtener_primera_fecha_venta()+'", "ultima_venta": "'+dao_economia.obtener_ultima_fecha_venta()+'"}'  

        return fechas_ventas