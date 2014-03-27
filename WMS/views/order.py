from flask import Blueprint, render_template, abort, \
                  request, session, flash, redirect, url_for
from WMS.app import db
from WMS.models import Order, OrderDetail, Account, Item
from WMS.models import str2datetime
from WMS.views import verify_login

import json

order = Blueprint('order', __name__)

# list all orders
@order.route('/list')
@verify_login
def list_all():
    orders_raw = Order.query.order_by(Order.date.desc()).all()
    orders = list()
    for o in orders_raw:
        order = dict(no=o.no, date=str(o.date.date()), \
                     place=o.place.place, id=o.id)
        if o.status == 0:
            order['status'] = 'unfinish'
        elif o.status == 1:
            order['status'] = 'finished'
        else:
            continue
        orders.append(order)
    return render_template("order-list.html", orders=orders)

# show order details
@order.route('/detail/<order_id>')
def detail(order_id):
    if session["status"] == "logined":
        order_raw = Order.query.filter_by(id=order_id).first()
        order = dict()
        order['no'] = order_raw.no
        order['date'] = str(order_raw.date)
        if order_raw.status == 0:
            order['status'] = 'unfinish'
        elif order_raw.status == 1:
            order['status'] = 'finished'
        else:
            order['status'] = 'delete'
        order['place'] = order_raw.place.place
        order['details'] = list()
        for d in order_raw.details:
            pass

        return render_template("order-detail.html", order=order)
    return redirect(url_for('accounts.login')) 

# show create page
@order.route('/create')
@verify_login
def create():
    return render_template("order-create.html")

# answer the quest to store data
@order.route('/create', methods=['POST'])
@verify_login
def perform_create():
    date = str2datetime(request.form['order_date'])
    no = request.form['order_no']
    details = json.loads(request.form['details'])

    if Order.query.filter_by(no=no).first():
        flash('Order Exist','error')
        return redirect(url_for('order.create'))

    # create an new order
    place_id = Account.query.filter_by(id=session['user_id']).first().place_id
    order = Order(no=no, place_id=place_id,date=date)
    db.session.add(order)
    db.session.commit()
    # add order details
    for d in details:
        number = d['number']
        description = d['description']
        # found the item or create a new item
        item = Item.query.filter_by(number=number).first()
        if not item:
            item = Item(number=number,description=description)
        # update the retail and whole price
        item.retail = d['retail']
        item.whole = d['whole']
        db.session.add(item)
        db.session.commit()

        for column in d['columns']:
            d = OrderDetail(item_id=item.id, order_id=order.id, \
                            size = column['size'], \
                            amount=column['amount'])
            db.session.add(d)
        db.session.commit()
    return redirect(url_for('order.list_all'))