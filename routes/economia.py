from flask import Blueprint, render_template,redirect,url_for

economia_bp = Blueprint('economia', __name__,url_prefix='/economia', template_folder='templates')


@economia_bp.route("/", methods=['GET'])
def dashboard():
    return render_template('pages/page-economia/dashboard.html')