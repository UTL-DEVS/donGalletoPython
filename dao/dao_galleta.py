from utils import db
from models import Galleta

def getAllGalletas():
    galletas = Galleta.query.filter_by(activo=1).all()
    print(f'gallletas: {galletas}')
    return galletas
