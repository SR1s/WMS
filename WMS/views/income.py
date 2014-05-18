#coding: utf8
from flask import Blueprint, render_template, abort, request, \
                  session, redirect, flash, url_for
from WMS.app import db
from WMS.models import Item, Income, Order, OrderDetail, IncomeDetail, Storage
from WMS.views import verify_login, sort_cal_all
from sqlalchemy import and_
import json


income = Blueprint("income", __name__)

# list all income
@income.route("/list")
@verify_login
def list_all():
    incomes = Income.query.order_by(Income.id.desc()).all()
    incomes = [dict(no=i.order.no, date=str(i.date.date()), \
                    id=i.id) \
               for i in incomes]
    return render_template("income-list.html", incomes=incomes)

'''
show the interface to user
'''
@income.route('/create')
@verify_login
def create():
    order_id = request.args.get('id', 0)
    order = Order.query.filter_by(id=order_id).first()
    order = order.to_dict()
    return render_template('income-create.html', order=order)

@income.route('/create', methods=['POST'])
@verify_login
def perform_create():
    ### Data Validity Start ###
    order_id = request.form.get('order_no', None)
    order = Order.query.filter_by(id=order_id).first()
    if ( order_id == None or order == None ):
        flash('订单号为空 或 订单不存在')
        return redirect(url_for('income.create'))
    income_details = json.loads(request.form['details'])
    if len(income_details)<1:
        flash('订单为空')
        return redirect(url_for('income.create'))

    order_details = Order.query_order_remain(order_id, raw=True)

    valid = dict()
    for detail in order_details:
        number, size = detail['number'], detail['size']
        item_id = detail['item_id']
        income = income_details.get(number)
        if income:
            income.setdefault('item_id', item_id)
            income = income['columns'].get(size, 0)
        else:
            income = 0
        detail['amount'] = detail['amount'] - income

        flag = valid.setdefault(number, {})
        flag[size] = detail['amount']

    # start to valid if item is not in order
    # or income amount excel the needed
    valid_status = True
    for (number, data) in income_details.items():
        valid_item = valid.get(number)
        if valid_item==None:
            valid_status = False
            flash("原订单不存在编号: %s 的物品。" % \
                      (number), 'error')
            continue
        for (size, amount) in data['columns'].items():
            if amount < 1:
                continue
            valid_size = valid_item.get(size)
            if valid_size == None:
                valid_status = False
                flash("原订单不存在编号: %s，尺寸: %s 的物品。" % \
                      (number, size), 'error')
            elif valid_size<0 :
                valid_status = False
                flash("编号: %s，尺寸: %s 物品的到货数量多于未到货数量。" % \
                      (number, size), 'error')

    #raise ValueError
    if valid_status == False:
        return redirect(url_for('income.create'))
    ### Data Validity End ###

    ### Assemble Data For Create IncomeOrder Start ###
    data = dict()
    data['order_id'] = order_id
    data['place_id'] = order.place_id
    data['details'] = list()
    for (number, detail) in income_details.items():
        item_id = detail['item_id']
        for (size, amount) in detail['columns'].items():
            if amount < 1 :
                continue
            item = dict(
                item_id = item_id,
                size = size,
                amount = amount,
            )
            data['details'].append(item)
    Income.create_an_order(data)
    flash('进货记录已添加')
    ### Assemble Data For Create IncomeOrder End   ###

    return redirect(url_for('order.list_all'))


@income.route('/detail/<int:income_id>')
def detail(income_id):
    income = Income.query.filter_by(id=income_id).first()
    if income == None:
        flash('不存在此订单')
        return redirect('index')
    income = dict(date=str(income.date.date()), \
                  no=income.order.no, \
                  details=income.details)
    details = dict()
    for d in income['details']:
        detail = details.setdefault(d.item.number,dict())
        detail['number'] = d.item.number
        detail['description'] = d.item.description
        columns = detail.setdefault('columns', list())
        columns.append(dict(size=d.size, amount=d.amount))
    for d in details:
        c = details[d]['columns']
        if len(c)<6:
            n = 7-len(c)
            for x in range(0,n):
                c.append(dict(size='-',amount=0))
        details[d]['sum'] = sort_cal_all(c)
    income['details'] = details
    #return json.dumps(income)
    return render_template('income-detail.html', income=income)

@income.route('/create_by_upload', methods=['POST'])
@verify_login
def create_by_upload():
    order_id = request.form.get('id', -1)
    if order_id == -1:
        flash('Order Number invaild')
        return redirect('order.list_all')
    return 'hello kitty'
