from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Order, OrderDetail
from WMS.views import verify_login

import json

order = Blueprint('order', __name__)

@order.route('/list')
@verify_login
def list_all():
    orders = Order.query.all()
    return render_template("order-list.html", orders=orders)

@order.route('/create')
@verify_login
def create():
    return render_template("order-create.html")

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
        d = OrderDetail(detail['number'], detail['description'], order.id, \
                        detail['size1'], detail['amount1'], \
                        detail['size2'], detail['amount2'], \
                        detail['size3'], detail['amount3'], \
                        detail['size4'], detail['amount4'], \
                        detail['size5'], detail['amount5'], \
                        detail['size6'], detail['amount6'], \
                        detail['retail'], detail['whole'], detail['total'] )
        db.session.add(d)
    db.session.commit()
    
    newOrder = Order.query.filter_by(id=order.id).first()
    return render_template("order-detail.html", order=newOrder)