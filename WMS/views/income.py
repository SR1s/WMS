from flask import Blueprint, render_template, abort, request, \
                  session, redirect, flash, url_for
from WMS.app import db
from WMS.models import Item, Income, Order, IncomeDetail
from WMS.views import verify_login
import json


income = Blueprint("income", __name__)

@income.route("/list")
@verify_login
def list():
    incomes = Income.query.all()
    return render_template("order-list.html")

@income.route('/create')
@verify_login
def create():
    orders = Order.query.all()
    return render_template('income-create.html', orders=orders)

@income.route('/create', methods=['POST'])
@verify_login
def perform_create():
    date = request.form['order_date']
    no = request.form['order_no']
    details_in = json.loads(request.form['details'])

    # check if order exist
    order = Order.query.filter_by(order_no=no).first()
    if order == None:
        flash('Error! Order did not exist!')
        return redirect(url_for('income.create'))

    # select details from order and store in an array using dictionary
    details_raw = [ dict(number=detail.number, \
                    size1=detail.size1, amount1=detail.amount1, \
                    size2=detail.size2, amount2=detail.amount2, \
                    size3=detail.size3, amount3=detail.amount3, \
                    size4=detail.size4, amount4=detail.amount4, \
                    size5=detail.size5, amount5=detail.amount5, \
                    size6=detail.size6, amount6=detail.amount6, ) \
                    for detail in order.details.all() ]
    # select income record
    incomes = Income.query.filter_by(order_no=no)
    # check how many order details need to be income  
    for income in incomes:
        # select exist detail from income
        details_exit = [ dict(number=detail.number, \
                    size1=detail.size1, amount1=detail.amount1, \
                    size2=detail.size2, amount2=detail.amount2, \
                    size3=detail.size3, amount3=detail.amount3, \
                    size4=detail.size4, amount4=detail.amount4, \
                    size5=detail.size5, amount5=detail.amount5, \
                    size6=detail.size6, amount6=detail.amount6, ) \
                    for detail in income.details.all() ]
        # calculating... 
        for detail_exit in details_exit:
            for detail_raw in details_raw:
                if detail_exit['number'] == detail_raw['number']:
                    i, j = 1, 1
                    for i in range(1,7):
                        for j in range(1,7):
                            size1 = "size"+str(i)
                            size2 = "size"+str(j)
                            amount1 = "amount"+str(i)
                            amount2 = "amount"+str(j)
                            if detail_raw[size1] == detail_exit[size2]:
                                detail_raw[amount1] = \
                                    detail_raw[amount1] - detail_exit[amount2]
    
    # check is the income amount match the need
    vaild = dict()
    for detail_in in details_in:
        vaild[detail_in['number']] = False
        for detail_raw in details_raw:
            if detail_in['number'] == detail_raw['number']:
                vaild[detail_in['number']] = True
                i, j = 1, 1
                for i in range(1,7):
                    for j in range(1, 7):
                        size1 = "size"+str(i)
                        size2 = "size"+str(j)
                        amount1 = "amount"+str(i)
                        amount2 = "amount"+str(j)
                        if detail_raw[size1] == detail_in[size2]:
                            detail_raw[amount1] = \
                                detail_raw[amount1] - int(detail_in[amount2])
                            isMatch = True
                            if detail_raw[amount1] < 0:
                                flash("Error! Amount not match!")
                                return redirect(url_for('income.create'))
    # if some is not in order items
    for (key, value) in vaild.items():
        if value == False:
            flash("Error, %s not in order!" % key)
            return redirect(url_for('income.create'))
    # store income and income details
    income = Income(order.order_no)
    db.session.add(income)
    db.session.commit()
    for detail_in in details_in:
        d = IncomeDetail(detail_in['number'], \
                         detail_in['description'], \
                         income.id, \
                         detail_in['size1'], detail_in['amount1'], \
                         detail_in['size2'], detail_in['amount2'], \
                         detail_in['size3'], detail_in['amount3'], \
                         detail_in['size4'], detail_in['amount4'], \
                         detail_in['size5'], detail_in['amount5'], \
                         detail_in['size6'], detail_in['amount6'] )
        db.session.add(d)
    db.session.commit()
    # then check if the order is finished
    isFinished = True
    for detail_raw in details_raw:
        i = 1
        for i in range(1, 7):
            if detail_raw['amount'+str(i)] > 0:
                isFinished = False
    order = Order.query.filter_by(order_no=no).first()
    if isFinished:
        flash('Order: %s is Finished!' % order.order_no)
        order.isFinished = 1
    else:
        order.isFinished = 0
    db.session.commit()
    return redirect(url_for('order.list_all'))