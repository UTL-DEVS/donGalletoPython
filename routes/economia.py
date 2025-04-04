from utils import Blueprint, render_template, redirect, request, login_required, current_user, flash, url_for, abort
from datetime import datetime
from controller import controller_economia
import json
from funcs import crear_log_user, crear_log_error

economia_bp = Blueprint('economia', __name__, url_prefix='/economia', template_folder='templates')

@economia_bp.route("/", methods=['GET'])
@login_required
def dashboard():
    try:
        if current_user.rol_user != 0:
            abort(404)
        fechas_ventas = controller_economia.obtener_fechas_ventas()
        lista_ventas_json=''
        if (fechas_ventas != None):
            print(f'fechas: {fechas_ventas}')
            if(request.args.get('dias_ventas') == None):
                mes_venta=json.loads(fechas_ventas)['ultima_venta']
                dias = 30
            else:
                mes_venta = ((request.args.get('mes_ventas')))
                dias =((request.args.get('dias_ventas')))
    
        lista_ventas = controller_economia.obtener_ventas_diarias(mes_venta, dias)
        lista_ventas_json = json.dumps([
            {
                "fecha_venta": venta.fecha.strftime("%Y-%m-%d"),  # Convertir datetime a string
                "total": venta.total,
                "estatus": venta.estado
            }
            for venta in lista_ventas
        ])
        crear_log_user(current_user.usuario, request.url)
        return render_template('pages/page-economia/dashboard.html',rango_fechas_ventas=fechas_ventas,lista_ventas=lista_ventas_json)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el panel económico", "danger")
        return redirect('/error')
    
    

@economia_bp.route('/nomina', methods=['GET'])
@login_required
def mostrar_nomina():
    anio = (datetime.now()).year
    mes = (datetime.now()).month 
    quincena=2
    if (datetime.now().day <= 15):
        quincena=1
    if request.method == 'GET':
        mes = request.args.get('mes', type=int)
        anio = request.args.get('anio', type=int)
        quincena = request.args.get('quincena', type=int, default=None)
     
    pagos, total_pagos = controller_economia.obtener_pagos(mes, anio, quincena)
    if (not pagos) and (request.args.get('mes', type=int) != None):
        flash("No hay pago de sueldos en el periodo seleccionado.", "error")
        return redirect(url_for('economia.mostrar_nomina'))
    return render_template('pages/page-economia/nomina.html', pagos=pagos, mes=mes, anio=anio, quincena=quincena,total_pagos=total_pagos)
    

@economia_bp.route('/nomina/sueldos', methods=['GET'])
@login_required
def mostrar_pagos_pendientes():
    empleados_no_pagados = controller_economia.obtener_empleados_no_pagados()

    return render_template('pages/page-economia/pago_nomina.html', empleados_sin_pago=empleados_no_pagados)

@economia_bp.route('/nomina/pago', methods=['GET'])
@login_required
def pagar_empleado():
    """Realiza el pago a un empleado específico"""
    id_empleado = request.args.get('id_emp')
    if controller_economia.verificar_pago_empleado(id_empleado):
        flash("Este empleado ya ha sido pagado en la quincena actual.", "error")
        return redirect(url_for('economia.mostrar_pagos_pendientes'))

    # Obtener sueldo del empleado
    empleado = controller_economia.obtener_empleado(id_empleado)
    if not empleado:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for('economia.mostrar_pagos_pendientes'))

    sueldo_calculado = (empleado.sueldo_empleado) * empleado.dias_laborales
    if (controller_economia.pagar_empleado(id_empleado, sueldo_calculado)):
        flash("Pago realizado con éxito.", "success")
    else:
        flash("Algo salió mal.", "error")
    return redirect(url_for('economia.mostrar_pagos_pendientes'))

    

    