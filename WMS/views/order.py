#coding: utf8
from datetime import datetime
import json

from flask import ( Blueprint, render_template, abort, 
                    request, session, flash, redirect, url_for, )
from WMS.app import db
from WMS.models import Account, Income, Item, Order, OrderDetail
from WMS.utils import readXls, str2datetime
from WMS.views import verify_login, chkstatus, sort_cal_all, chkstatus


order = Blueprint('order', __name__)

# list all orders
@order.route('/list')
@verify_login
def list_all():
    orders = [ order.to_dict() 
               for order in Order.query.order_by(Order.date.desc()).all()]
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
        order_details_json = json.dumps(order['details'].values())
        incomes = [ i.to_dict() \
                    for i in Income.query.filter_by(order_id=order_id).all()]
        return render_template("order-detail.html", 
                                order=order,
                                order_details_json=order_details_json,
                                incomes=incomes,)
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
    data = dict()
    data['order_no'] = request.form['order_no']
    data['place_id'] = session['place_id']
    data['date'] = str2datetime(request.form['order_date'])
    if data['date']==None:
        data['date']=datetime.utcnow()
    data['items'] = json.loads(request.form['details'])
    #for item in data['items']:
    #    item['columns'].pop('')
    
    if Order.query.filter_by(no=data['order_no'].upper()).first():
        flash('Excel file format is not correct Or Order already Exist', 'error')
        return redirect(url_for('order.list_all'))

    Order.create_an_order(data)
    flash('Success adding order')
    return redirect(url_for('order.list_all'))

@order.route('/create_by_upload', methods=['POST'])
def create_by_upload():
    if request.files['file'].filename.split('.')[-1] not in ('xls', 'xlsx'):
        flash('Upload File illegal!')
        return redirect(url_for('index'))

    request.files['file'].save('temp.xls')
    data = readXls('temp.xls', 0)
    
    if data['error'] \
       or Order.query.filter_by(no=data['order_no'].upper()).first():
        flash('Excel file format is not correct Or Order already Exist', 'error')
        return redirect(url_for('order.list_all'))
    
    data['place_id'] = session['place_id']
    Order.create_an_order(data)
    flash('Success adding order')
    return redirect(url_for('order.list_all'))