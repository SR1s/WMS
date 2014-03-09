from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Order
from WMS.views import verify_login

order = Blueprint('order', __name__)

@order.route('/all')
@verify_login
def all():
    orders = Order.query.all()
    return str(orders)

@orders.route('/create')
@verify_login
def create():
    pass

@orders.route('/create', methods=['POST'])
@verify_login
def perform_create():
    pass