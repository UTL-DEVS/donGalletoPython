from flask import Blueprint, render_template
import json
from forms import *
from models import Proveedor
from dao import dao_galleta

galleta_bp = Blueprint('galleta', __name__,url_prefix='/galleta', template_folder='templates')

@galleta_bp.route('/getAllGalletas', methods=['POST','GET'])
def mostrar_proveedores():
    lstGalletas = dao_galleta.getAllGalletas()
    return lstGalletas
