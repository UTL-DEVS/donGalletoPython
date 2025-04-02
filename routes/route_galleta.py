# this module is only to galleta crud

from utils import Blueprint, request, render_template


route_galleta = Blueprint('galleta_route', __name__,  template_folder='templates')

@route_galleta.route('/galleta_home')
def galleta_home():
    return render_template('pages/page-galleta/galletas.html')
