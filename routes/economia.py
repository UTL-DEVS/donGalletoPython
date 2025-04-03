from utils import Blueprint, render_template, redirect, flash, db, request, login_required, current_user, abort
from controller import controller_economia
import json
from funcs import crear_log_user, crear_log_error

economia_bp = Blueprint('economia', __name__, url_prefix='/economia', template_folder='templates')

@economia_bp.route("/", methods=['GET'])
@login_required
def dashboard():
    if current_user.rol_user != 0:
        abort(404)
    
    try:
        crear_log_user(current_user.usuario, request.url)

        fechas_ventas = controller_economia.obtener_fechas_ventas()
        print(f'fechas: {fechas_ventas}')
        
        if request.args.get('dias_ventas') == None:
            mes_venta = json.loads(fechas_ventas)['ultima_venta']
            dias = 30
        else:
            mes_venta = request.args.get('mes_ventas')
            dias = request.args.get('dias_ventas')
        
        lista_ventas = controller_economia.obtener_ventas_diarias(mes_venta, dias)
        lista_ventas_json = json.dumps([
            {
                "fecha_venta": venta.fecha.strftime("%Y-%m-%d"),
                "total": venta.total,
                "estatus": venta.estado
            }
            for venta in lista_ventas
        ])
        
        for v in lista_ventas:
            print(f'F: {v.fecha}')
            print(f't: {v.total}')

        return render_template(
            'pages/page-economia/dashboard.html',
            rango_fechas_ventas=fechas_ventas,
            lista_ventas=lista_ventas_json
        )

    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        flash("❌ Error al cargar el panel económico", "danger")
        return redirect('/error')