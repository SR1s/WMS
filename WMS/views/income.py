from flask import Blueprint, render_template, abort, request, \
                  session, redirect
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
    return redirect(url_for('income.create'))