from flask import Blueprint, render_template, abort, request
from WMS.models import Account
from WMS.app import db
from WMS.models import Place
from WMS.utils import md5

accounts = Blueprint("accounts",__name__)

@accounts.route("/login")
def login():
    return render_template("login.html")

@accounts.route("/login", methods=['POST'])
def perform_login():
    user_no = request.form['user_no']
    user_ps = md5(request.form['user_ps'])
    user = Account.query.filter_by(user_no=user_no,user_ps=user_ps).first()
    if user:
        return "you have log in!"
    else:
        return "error no or password"

@accounts.route("/create")
def create():
    pass