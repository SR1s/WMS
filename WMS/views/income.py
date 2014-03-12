from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Item, Income
from WMS.views import verify_login


income = Blueprint("income", __name__)

@income.route("/list")
@verify_login
def list():
	incomes = Income.query.all()
	return render_template("order-list.html")
