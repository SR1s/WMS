from flask import Blueprint, render_template, abort, flash, \
                    request, session, redirect, url_for
from WMS.app import db
from WMS.forms.accounts import LoginForm
from WMS.models import Place, Account
from WMS.utils import md5
from WMS.views import verify_login

from datetime import datetime

accounts = Blueprint("accounts",__name__)

@accounts.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@accounts.route("/login", methods=['POST'])
def perform_login():
    form = LoginForm(request.form)
    status = "error"
    message = "Error! Wrong username or password."
    if form.validate():
        user_no = request.form['user_no']
        user_ps = md5(request.form['user_ps'])
        user = Account.query.filter_by(user_no=user_no,user_ps=user_ps).first()
        if user:
            status = "normal"
            session["user_no"] = user_no
            session["user_id"] = user.id
            session["place_id"] = user.place.id
            session["time"] = datetime.utcnow()
            message = "You have logined!"
    flash(message, category=status)
    return redirect(url_for("index"))

@accounts.route("/create")
@verify_login
def create():
    return session['status']


@accounts.route("/logout")
def logout():
    session["user_id"] = None
    session["user_no"] = None
    session["time"] = None
    return "you have logout!\n status: %s \n user_no: %s \n" % \
            (session["status"], session["user_no"])