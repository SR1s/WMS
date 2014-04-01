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

# store the income record
@income.route('/create')
@verify_login
def create():
    orders = Order.query.filter_by(status=0).order_by(Order.date.desc()).all()
    if orders and len(orders)>0:
         return render_template('income-create.html', orders=orders)
    flash('目前没有未到货完毕的订单', 'error')
    return redirect(url_for('index'))

# need rework
@income.route('/create', methods=['POST'])
@verify_login
def perform_create():
    place_id = session['place_id']
    no = request.form.get('order_no', None)
    if no == None:
      flash('订单号不能为空')
      return redirect(url_for('income.create'))
    postdata = json.loads(request.form['details'])

    # check if order exist
    order = Order.query.filter_by(id=no).first()
    if order == None:
        flash('订单不存在')
        return redirect(url_for('income.create'))

    # select details from order and store in an array using dictionary
    details_order = [dict(size=d.size, amount=d.amount, number=d.item.number, id=d.item.id) \
                     for d in OrderDetail.query.filter_by(order_id=no).all()]

    # select income record
    incomes = Income.query.filter_by(order_id=no).all()
    # check how many order details need to be income
    for income in incomes:
        # select exist detail from income
        details_income = IncomeDetail.query.filter_by(income_id=income.id).all()
        details_income = [dict(size=d.size, amount=d.amount, number=d.item.number) \
                          for d in details_income]
        for detail_income in details_income:
            for detail_order in details_order:
                if detail_income['number'] == detail_order['number'] and \
                   detail_income['size'] == detail_order['size']:
                    detail_order['amount'] = detail_order['amount'] - detail_income['amount']

    # check is the income amount match the need
    vaild = dict()
    for (k,d) in postdata.items():
        vaild[d['number']] = False
        for detail_order in details_order:
            if d['number'] == detail_order['number']:
                d['id'] = detail_order['id']
                for detail in d['columns']:
                    if detail['size'] == detail_order['size']:
                        detail_order['amount'] = detail_order['amount'] - int(detail['amount'])
                    vaild[d['number']] = True

    # if some is not in order items
    haveError = False
    for (key, value) in vaild.items():
        if value == False:
            haveError = True
            flash("订单不存在货物%s!" % key, 'error')
    for detail in details_order:
        if detail['amount']<0:
            flash('货号%s:尺寸%s的货物到货数量大于未到货数量' % (detail['number'], detail['size']), 'error')
            haveError = True
    if haveError:
        return redirect(url_for('income.create'))

    # store income and income details
    income = Income(no)
    db.session.add(income)
    db.session.commit()
    for (k,d) in postdata.items():
        for detail in d['columns']:
            inde = IncomeDetail(item_id=d['id'], income_id=income.id, \
                                size=detail['size'], amount=detail['amount'])
            storage = Storage.query.filter(and_(Storage.item_id==d['id'], Storage.size==detail['size'], Storage.place_id==place_id)).first()
            if storage:
                storage.amount = storage.amount + int(detail['amount'])
            else:
                storage = Storage(size=detail['size'], amount=detail['amount'], item_id=d['id'], place_id=place_id)
            db.session.add(storage)
            db.session.add(inde)
    db.session.commit()

    # then check if the order is finished
    isFinished = True
    for detail_order in details_order:
        if detail_order['amount']>0:
            isFinished = False
    order = Order.query.filter_by(id=no).first()
    if isFinished:
        flash('订单号为 %s 的订单已到货完毕' % order.no)
        order.status = 1
    else:
        order.status = 0
    db.session.commit()
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
