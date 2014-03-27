from flask import Blueprint, render_template, abort, request, \
                  session, redirect, flash, url_for
from WMS.app import db
from WMS.models import Item, Income, Order, OrderDetail, IncomeDetail
from WMS.views import verify_login
import json


income = Blueprint("income", __name__)

# list all income
@income.route("/list")
@verify_login
def list():
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
    flash('No unfinish order!', 'error')
    return redirect(url_for('index'))


# need rework
@income.route('/create', methods=['POST'])
@verify_login
def perform_create():
    no = request.form['order_no']
    postdata = json.loads(request.form['details'])

    # check if order exist
    order = Order.query.filter_by(id=no).first()
    if order == None:
        flash('Error! Order did not exist!')
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
    for d in postdata:
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
            flash("Error, %s not in order!" % key, 'error')
    for detail in details_order:
        if detail['amount']<0:
            flash('Item %s:%s amount Error' % (detail['number'], detail['size']), 'error')
            haveError = True
    if haveError:
        return redirect(url_for('income.create'))

    # store income and income details
    income = Income(no)
    db.session.add(income)
    db.session.commit()
    for d in postdata:
        for detail in d['columns']:
            inde = IncomeDetail(item_id=d['id'], income_id=income.id, \
                                size=detail['size'], amount=detail['amount'])
            db.session.add(inde)
    db.session.commit()

    # then check if the order is finished
    isFinished = True
    for detail_order in details_order:
        if detail_order['amount']>0:
            isFinished = False
    order = Order.query.filter_by(id=no).first()
    if isFinished:
        flash('Order: %s is Finished!' % order.no)
        order.status = 1
    else:
        order.status = 0
    db.session.commit()
    return redirect(url_for('order.list_all'))

@income.route('/detail/<int:income_id>')
def detail(income_id):
    income = Income.query.filter_by(id=income_id).first()
    return render_template('income-detail.html', income=income)