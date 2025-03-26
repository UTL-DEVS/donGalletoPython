# this module to service to create new blueprint to client
from utils import *

client_bp = Blueprint('client', __name__, template_folder='templates')

@client_bp.route('/client')
def index_client():
    return render_template('pages/client.html')

