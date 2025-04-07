from dao import dao_economia
from datetime import datetime

def obtener_ventas_diarias(mes, dias):
    return dao_economia.obtener_ventas_por_mes(mes, dias)

def optener_ventas_galletas_masvendidad(mes):
    return dao_economia.obtener_ventas_galletas_mas_vendidas(mes)

def obtener_fechas_ventas():
        fechas_ventas = None  
        primera_venta =dao_economia.obtener_primera_fecha_venta()
        if(primera_venta != None):
            fechas_ventas = '{"primera_venta": "'+primera_venta+'", "ultima_venta": "'+dao_economia.obtener_ultima_fecha_venta()+'"}'  
        
        return fechas_ventas

def obtener_pagos(mes, anio, semana):
    return dao_economia.obtener_pagos_con_total(mes,anio,semana)

def obtener_empleados_no_pagados():
    mes = datetime.now().month
    anio = datetime.now().year  
    return dao_economia.obtener_empleados_no_pagados(mes,anio)

def verificar_pago_empleado(id_empleado):
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    hoy = datetime.now().day
    quincena_actual = 1 if hoy <= 15 else 2
    return dao_economia.verificar_pago_empleado(id_empleado, quincena_actual, mes_actual, anio_actual)

def obtener_empleado(id_empleado):
    return dao_economia.obtener_empleado(id_empleado)

def pagar_empleado(id_empleado, sueldo_calculado):
     return dao_economia.pagar_empleado(id_empleado, sueldo_calculado)


def agregar_gasto(tipo, monto, fecha, id_usuario):
    return dao_economia.agregar_gasto(tipo, monto, fecha, id_usuario)

def obtener_gastos_por_mes(mes):
    return dao_economia.obtener_gastos_por_mes(mes)