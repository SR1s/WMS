from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Order
from WMS.views import verify_login

order = Blueprint('order', __name__)

@order.route('/list')
@verify_login
def list():
    orders = Order.query.all()
    return None

@order.route('/create')
@verify_login
def create():
    return render_template("create-order.html")

@order.route('/create', methods=['POST'])
@verify_login
def perform_create():
    return render_template("create-order.html")