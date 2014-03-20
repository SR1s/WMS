from flask import Blueprint, render_template, abort, request, \
                  session, redirect, flash
from WMS.app import db
from WMS.models import Item, Income, Order
from WMS.views import verify_login


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

    order = Order.query.filter_by(order_no=no).first()
    if order == None:
        flash('Error! Order did not exist!')
        return redirect(url_for('income.create'))
    details_raw = order.details.all()
    incomes = Income.query.filter_by(order_no=no)
    for income in incomes:
        for detail_exit in incomes.details.all():
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
                                detail_raw[amount1] - detail_in[amount2]
                            isMatch = True
                            if detail_raw[amount1] < 0:
                                flash("Error! Amount not match!")
                                return redirect(url_for('income.create'))
    for (key, value) in vaild.items():
        if value == False:
            flash("Error, %s not in order!")
            return redirect(url_for('income.create'))

    for detail_in in details_in:
        d = IncomeDetail(detail['number'], detail['description'], order.id, \
                        detail['size1'], detail['amount1'], \
                        detail['size2'], detail['amount2'], \
                        detail['size3'], detail['amount3'], \
                        detail['size4'], detail['amount4'], \
                        detail['size5'], detail['amount5'], \
                        detail['size6'], detail['amount6'] )
        db.session.add(d)
    db.session.commit()
    isFinished = True
    for detail_raw in details_raw:
        i = 1
        for i in range(1, 7):
            if detail_raw['amount'+str(i)] > 0:
                isFinished = False
    order = Order.query.filter_by(order_no=no).first()
    if isFinished:
        order.isFinished = 1
    else:
        order.isFinished = 0
    db.session.commit()
    return redirect(url_for('income.create'))