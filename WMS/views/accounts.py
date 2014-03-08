from flask import Blueprint, render_template, abort, request
from WMS.app import db
from WMS.forms.accounts import LoginForm
from WMS.models import Place, Account
from WMS.utils import md5

accounts = Blueprint("accounts",__name__)

@accounts.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@accounts.route("/login", methods=['POST'])
def perform_login():
    form = LoginForm(request.form)
    if form.validate():
        user_no = request.form['user_no']
        user_ps = md5(request.form['user_ps'])
        user = Account.query.filter_by(user_no=user_no,user_ps=user_ps).first()
        if user:
            return "you have log in!"
        else:
            return "error no or password"
    return render_template("login.html", form=form)

@accounts.route("/create")
def create():
    pass