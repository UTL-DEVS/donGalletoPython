from utils import db, Blueprint, redirect, render_template, request
from utils import login_required, current_user

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaCompra = db.Colum(db.String(), nullable=False)