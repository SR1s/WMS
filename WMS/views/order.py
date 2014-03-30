#coding: utf8
from flask import Blueprint, render_template, abort, \
                  request, session, flash, redirect, url_for
from WMS.app import db
from WMS.models import Order, OrderDetail, Account, Item
from WMS.models import str2datetime
from WMS.views import verify_login, chkstatus, cal_all, mycmp, chkstatus

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
                     place=o.place.place, id=o.id, status=chkstatus(o.status))
        orders.append(order)
    return render_template("order-list.html", orders=orders)

# show order details
@order.route('/detail/<order_id>')
def detail(order_id):
    if True:
        order = Order.query.filter_by(id=order_id).first()
        if order:
            details = OrderDetail.query.filter_by(order_id=order.id).all()
            order=dict(number=order.no, date=str(order.date.date()), \
                       status=chkstatus(order.status))
            order['details'] = dict()
            for d in details:
                detail = order['details'].setdefault(d.item.number, dict())
                detail['number'] = d.item.number
                detail['description'] = d.item.description
                columns = detail.setdefault('columns', list())
                columns.append(dict(size=d.size, amount=d.amount))
            for (k, v) in order['details'].items():
                v['sum']=cal_all(v['columns'])
                v['columns'].sort(mycmp)
        else:
            flash('不存在此订单')
            return redirect(url_for('items.list_all'))
        #return json.dumps(order)
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
        flash('编号%s的订单已存在' % no,'error')
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