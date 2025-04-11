from utils import db, func,extract, func
from models import Nomina, Empleado, Persona, Galleta, DetalleVenta, GastoOperacion
from models.ProcesoVenta import ProcesoVenta
from datetime import datetime, timedelta


def obtener_ventas_por_mes(mes, dias): 
    # Convertir el mes en un rango de fechas
    mes_numero, anio = map(int, str(mes).split('/'))
    
    ultimo_dia = datetime(anio, mes_numero, 1).replace(day=28) + timedelta(days=4)
    ultimo_dia = ultimo_dia - timedelta(days=ultimo_dia.day)  # Último día del mes
    primer_dia = ultimo_dia - timedelta(days=int(dias) - 1)

    # Consulta agrupada por día
    resultados = (
        db.session.query(
            func.date(ProcesoVenta.fecha).label("fecha_venta"),
            func.sum(ProcesoVenta.total).label("total_dia")
        )
        .filter(ProcesoVenta.fecha.between(primer_dia, ultimo_dia))
        .group_by(func.date(ProcesoVenta.fecha))
        .order_by(func.date(ProcesoVenta.fecha))
        .all()
    )
    # Retorna una lista de tuplas (fecha_venta, total_dia)
    return resultados


def obtener_galletas_mas_vendidas_del_mes(mes):
    mes_numero, anio = map(int, mes.split('/'))
    primer_dia = datetime(anio, mes_numero, 1)
    if mes_numero == 12:
        siguiente_mes = datetime(anio + 1, 1, 1)
    else:
        siguiente_mes = datetime(anio, mes_numero + 1, 1)
    ultimo_dia = siguiente_mes - timedelta(seconds=1)

    resultados = (
        db.session.query(
            DetalleVenta.galleta_id,
            db.func.sum(DetalleVenta.cantidad).label('total_vendida'),
            Galleta.nombre
        )
        .join(DetalleVenta.proceso_venta)
        .join(DetalleVenta.galleta)
        .filter(ProcesoVenta.fecha.between(primer_dia, ultimo_dia))
        .group_by(DetalleVenta.galleta_id, Galleta.nombre)
        .order_by(db.desc('total_vendida'))
        .all()
    )

    return resultados


def obtener_primera_fecha_venta():
    primera_fecha_venta = (db.session.query(func.date_format(ProcesoVenta.fecha,  "%m/%Y"))
            .order_by(ProcesoVenta.fecha.asc())
            .limit(1)
            .scalar())
    return primera_fecha_venta
        
def obtener_ultima_fecha_venta():
    ultima_fecha_venta = (db.session.query(func.date_format(ProcesoVenta.fecha,  "%m/%Y"))
        .order_by(ProcesoVenta.fecha.desc())
        .limit(1)
        .scalar()
        )
    return ultima_fecha_venta

# Nómina

def obtener_pagos_con_total(mes, anio, quincena=None):
    """Obtiene los pagos de nómina con nombre del empleado, cantidad pagada y fecha, además del total"""
    
        # Si no se especifica mes o año, obtener el último mes y año con pagos
    if mes is None or anio is None:
        ultima_fecha = db.session.query(Nomina.fecha_pago).order_by(Nomina.fecha_pago.desc()).first()
        if ultima_fecha:
            mes = ultima_fecha.fecha_pago.month
            anio = ultima_fecha.fecha_pago.year
        else:
            return [], 0  # No hay registros

    query = db.session.query(
        Persona.nombre,  # Nombre del empleado
        Nomina.cantidad_pagada,
        Nomina.fecha_pago,
        func.sum(Nomina.cantidad_pagada).over().label("total_pagos")  # Suma total de los pagos
    ).join(Empleado, Empleado.id_empleado == Nomina.id_empleado).join(Persona, Persona.id_persona == Empleado.id_persona
    ).filter(
        extract('month', Nomina.fecha_pago) == mes,
        extract('year', Nomina.fecha_pago) == anio
    )
    # Filtrar por quincena si se especifica
    if quincena == 1:
        query = query.filter(extract('day', Nomina.fecha_pago) <= 15)
    elif quincena == 2:
        query = query.filter(extract('day', Nomina.fecha_pago) > 15)

    pagos = query.all()  # Obtener los resultados

    total_pagos = pagos[0].total_pagos if pagos else 0  # Obtener el total de la suma

    return pagos, total_pagos

def obtener_empleados_no_pagados(mes, anio):
    """Consulta empleados que aún no han recibido pago en la quincena actual."""
    hoy = datetime.now().day
    quincena_actual = 1 if hoy <= 15 else 2  # Determinar la quincena en curso

    # Subconsulta: Obtiene IDs de empleados que YA han sido pagados en la quincena actual
    subquery_pagados = db.session.query(Nomina.id_empleado).filter(
        extract('month', Nomina.fecha_pago) == mes,
        extract('year', Nomina.fecha_pago) == anio,
        (extract('day', Nomina.fecha_pago) <= 15 if quincena_actual == 1 else extract('day', Nomina.fecha_pago) > 15)
    ).subquery()

    # Consulta principal: Obtiene empleados que NO están en la subconsulta de pagados
    query = db.session.query(
        Empleado.id_empleado,
        Persona.nombre,  # Obtener el nombre del empleado
        (Empleado.sueldo_empleado  * Empleado.dias_laborales).label("sueldo_calculado")  # Cálculo del sueldo
    ).join(Persona, Empleado.id_persona == Persona.id_persona
    ).filter(~Empleado.id_empleado.in_(subquery_pagados))  # Filtrar empleados que no han sido pagados

    return query.all()

def verificar_pago_empleado(id_empleado, quincena_actual, mes_actual, anio_actual):
     # Verificar que el empleado no haya sido pagado en esta quincena
     return  Nomina.query.filter_by(
        id_empleado=id_empleado
    ).filter(
        extract('month', Nomina.fecha_pago) == mes_actual,
        extract('year', Nomina.fecha_pago) == anio_actual,
        (extract('day', Nomina.fecha_pago) <= 15 if quincena_actual == 1 else extract('day', Nomina.fecha_pago) > 15)
    ).first()

def obtener_empleado(id_empleado):
     return Empleado.query.get(id_empleado)

def pagar_empleado(id_empleado, sueldo_calculado):
     # Insertar el pago en la nómina
    nuevo_pago = Nomina(
        id_empleado=id_empleado,
        cantidad_pagada=sueldo_calculado
    )
    db.session.add(nuevo_pago)
    db.session.commit()
    return nuevo_pago.id_nomina

def agregar_gasto(tipo, monto, fecha, id_usuario):
    gasto = GastoOperacion(tipo=tipo, monto=monto, fecha=fecha, id_usuario=id_usuario)
    db.session.add(gasto)
    db.session.commit()

def obtener_gastos_por_mes(mes):  # formato 'MM/YYYY'
    mes_numero, anio = map(int, mes.split('/'))
    from datetime import date
    inicio = date(anio, mes_numero, 1)
    fin = date(anio, mes_numero, 28) + timedelta(days=4)
    fin = fin - timedelta(days=fin.day - 1)

    return db.session.query(GastoOperacion).filter(
        GastoOperacion.fecha.between(inicio, fin)
    ).all()
    

