from flask import Blueprint, render_template, request
import json
from forms import *
from models import Proveedor
from dao import dao_galleta
from funcs import crear_log_user, crear_log_error
from utils import login_required, current_user, abort

galleta_bp = Blueprint('galleta', __name__,url_prefix='/galleta', template_folder='templates')

@galleta_bp.route('/getAllGalletas', methods=['POST','GET'])
@login_required
def mostrar_proveedores():
    try:
        crear_log_user(current_user.usuario, request.url)
        lstGalletas = dao_galleta.getAllGalletas()
        return lstGalletas
    except Exception as e:
        crear_log_error(current_user.usuario, str(e))
        return {'error': 'Ocurrió un error al obtener las galletas'}, 500
