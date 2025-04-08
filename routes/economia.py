from utils import Blueprint, render_template, redirect, request, login_required, current_user, flash, url_for, abort
from datetime import datetime
from controller import controller_economia
import json
from forms.form_gastoOperacion import GastoForm
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
        return redirect('/economia')

    
    

@economia_bp.route('/nomina', methods=['GET'])
@login_required
def mostrar_nomina():
    anio = None
    mes = None
    quincena=2
    fecha_sel=None
    if (datetime.now().day <= 15):
        quincena=1
    if request.args.get('fechaSel') != None:
        fecha_sel = request.args.get('fechaSel')
        print(f'fecha sel: {fecha_sel}')
        anio,mes = map(str, str(fecha_sel).split('-'))
        #mes = request.args.get('mes', type=int)
        #anio = request.args.get('anio', type=int)
        quincena = request.args.get('quincena', type=int, default=None)
     
    pagos, total_pagos = controller_economia.obtener_pagos(mes, anio, quincena)
    if (not pagos) and (request.args.get('mes', type=int) != None):
        flash("No hay pago de sueldos en el periodo seleccionado.", "error")
        return redirect('/economia/nomina')
    return render_template('pages/page-economia/nomina.html', f=fecha_sel,pagos=pagos, mes=mes, anio=anio, quincena=quincena,total_pagos=total_pagos)
    

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



    
@economia_bp.route("/gastos", methods=['GET', 'POST'])
@login_required
def registrar_gastos():
    if current_user.rol_user != 0:
        abort(404)

    form = GastoForm()  # Aquí va arriba

    try:
        crear_log_user(current_user.usuario, request.url)

        if form.validate_on_submit():
            controller_economia.agregar_gasto(
                form.tipo.data,
                float(form.monto.data),
                form.fecha.data,
                current_user.id  # ✅ Ya corregido
            )
            flash("✅ Gasto registrado correctamente", "success")
            return redirect(url_for('economia.registrar_gastos'))
        return render_template("pages/page-economia/gastos.html", form=form)
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("❌ Ha ocurrido un error inesperado", "danger")

    return render_template("pages/page-economia/gastos.html", form=form)



# DASHBOARD DE GASTOS OPERATIVOS

@economia_bp.route("/gastos_dashboard", methods=['GET'])
@login_required
def dashboard_gastos():
    if current_user.rol_user != 0:
        abort(404)
    try:
        crear_log_user(current_user.usuario, request.url)

        mes = request.args.get('mes')
        if not mes:
            from datetime import datetime
            hoy = datetime.today()
            mes = f"{hoy.month:02d}/{hoy.year}"

        gastos = controller_economia.obtener_gastos_por_mes(mes)

        # Convertimos los objetos GastoOperacion a diccionarios
        gastos_dict = [
            {
                "tipo": gasto.tipo,
                "monto": gasto.monto,
                "fecha": gasto.fecha.strftime('%Y-%m-%d')
            } for gasto in gastos
        ]

        return render_template(
            "pages/page-economia/dashboard_gastos.html",
            lista_gastos=gastos_dict,
            mes_seleccionado=f"{mes.split('/')[1]}-{mes.split('/')[0]}"  # formato YYYY-MM
        )

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("Error al cargar el dashboard de gastos", "danger")
        return redirect(url_for('economia.dashboard'))
    