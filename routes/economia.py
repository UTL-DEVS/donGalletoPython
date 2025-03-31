from flask import Blueprint, render_template,request
from controller import controller_economia
import json

economia_bp = Blueprint('economia', __name__,url_prefix='/economia', template_folder='templates')


@economia_bp.route("/", methods=['GET'])
def dashboard():
    fechas_ventas = controller_economia.obtener_fechas_ventas()
    print(f'fechas: {fechas_ventas}')
    if(request.args.get('dias_ventas') == None):
        mes_venta=json.loads(fechas_ventas)['ultima_venta']
        dias = 30
    else:
        mes_venta = ((request.args.get('mes_ventas')))
        dias =((request.args.get('dias_ventas')))
    print(f'M: {mes_venta}')
    print(f'D: {dias}')
    lista_ventas = controller_economia.obtener_ventas_diarias(mes_venta, dias)
    lista_ventas_json = json.dumps([
        {
            "fecha_venta": venta.fecha_venta.strftime("%Y-%m-%d"),  # Convertir datetime a string
            "total_venta": venta.total_venta,
            "estatus": venta.estatus
        }
        for venta in lista_ventas
    ])

    return render_template('pages/page-economia/dashboard.html',rango_fechas_ventas=fechas_ventas,lista_ventas=lista_ventas_json)