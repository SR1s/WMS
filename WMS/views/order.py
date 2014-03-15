from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Order, OrderDetail
from WMS.views import verify_login

import json

order = Blueprint('order', __name__)

@order.route('/list')
@verify_login
def list_all():
    orders_raw = Order.query.all()
    orders = list()
    for order_raw in orders_raw:
        order = dict()
        order['order_no'] = order_raw.order_no
        order['date'] = order_raw.date
        order['details'] = order_raw.details.all()
        orders.append(order)
    return str(orders)

@order.route('/create')
@verify_login
def create():
    return render_template("create-order.html")

@order.route('/create', methods=['POST'])
@verify_login
def perform_create():
    date = request.form['order_date']
    no = request.form['order_no']
    order = Order(no, date=date)
    db.session.add(order)
    db.session.commit()
    details = json.loads(request.form['details'])
    for detail in details:
        d1 = OrderDetail(detail['number'], detail['size1'], detail['description'], \
                         detail['amount1'], order.id)
        d2 = OrderDetail(detail['number'], detail['size2'], detail['description'], \
                         detail['amount2'], order.id)
        d3 = OrderDetail(detail['number'], detail['size3'], detail['description'], \
                         detail['amount3'], order.id)
        d4 = OrderDetail(detail['number'], detail['size4'], detail['description'], \
                         detail['amount4'], order.id)
        d5 = OrderDetail(detail['number'], detail['size5'], detail['description'], \
                         detail['amount5'], order.id)
        d6 = OrderDetail(detail['number'], detail['size6'], detail['description'], \
                         detail['amount6'], order.id)
        db.session.add(d1)
        db.session.add(d2)
        db.session.add(d3)
        db.session.add(d4)
        db.session.add(d5)
        db.session.add(d6)
    db.session.commit()
    
    newOrder = Order.query.filter_by(id=order.id).first()
    return str(newOrder) + str(newOrder.details.all())
    return render_template("create-order.html")