#coding: utf8
from datetime import datetime
import json

from flask import Blueprint, render_template, abort, \
                  request, session, flash, redirect, url_for
from WMS.app import db
from WMS.models import Order, OrderDetail, Account, Item
from WMS.models import str2datetime
from WMS.utils import readXls
from WMS.views import verify_login, chkstatus, sort_cal_all, chkstatus


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
    return render_template("order-list.html", orders=orders, basic=dict())

# show order details
@order.route('/detail/<order_id>')
def detail(order_id):
    if True:
        order = Order.query.filter_by(id=order_id).first()
        if order:
            order = Order.query_order(order.id, with_order=True)
        else:
            flash('不存在此订单')
            return redirect(url_for('items.list_all'))
        return render_template("order-detail.html", order=order)
    return redirect(url_for('accounts.login'))

# show create page
@order.route('/create')
@verify_login
def create():
    return render_template("order-create.html")

@order.route('/remain')
@verify_login
def remain():
    order_id = request.args.get('id', -1)
    if order_id == -1 :
        raise ValueError
    order = Order.query_order_remain(order_id, with_order=True)
    return render_template('order-remain.html', order=order)

# answer the quest to store data
@order.route('/create', methods=['POST'])
@verify_login
def perform_create():
    info = dict()
    info['number'] = request.form['order_no']
    info['date'] = str2datetime(request.form['order_date'])
    if info['date']==None:
        info['date']=datetime.utcnow()
    info['items'] = json.loads(request.form['details'])
    return _handle_create_request(info)

@order.route('/create_by_upload', methods=['POST'])
def create_by_upload():
    if request.files['file'].filename.split('.')[-1] not in ('xls', 'xlsx'):
        flash('Upload File illegal!')
        return redirect(url_for('index'))
    request.files['file'].save('temp.xls')
    return _handle_create_request(readXls('temp.xls', 0))

def _handle_create_request(info):
    if info.setdefault('status', 'normal')=='error':
        flash('data incorrect.')
        return redirect(url_for('order.create'))

    no = info['number']
    date = info['date']
    details = info['items']

    if Order.query.filter_by(no=no).first():
        flash('编号%s的订单已存在' % no,'error')
        return redirect(url_for('order.create'))

    # create an new order
    place_id = Account.query.filter_by(id=session['user_id']).first().place_id
    order = Order(no=no, place_id=place_id,date=date)
    db.session.add(order)
    db.session.commit()
    # add order details
    for (number, d) in details.items():
        number = d['number']
        description = d.get('description', '')
        # found the item or create a new item
        item = Item.query.filter_by(number=number).first()
        if not item:
            item = Item(number=number,description=description)
        # update the retail and whole price
        item.retail = d.get('retail', 0)
        item.whole = d.get('whole', 0)
        db.session.add(item)
        db.session.commit()

        for column in d['columns']:
            d = OrderDetail(item_id=item.id, order_id=order.id, \
                            size = column['size'], \
                            amount=column['amount'])
            db.session.add(d)
        db.session.commit()
    return redirect(url_for('order.list_all'))