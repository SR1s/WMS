#coding: utf8

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
    message = "帐号/密码错误。"
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
            message = "登录成功"
            
            if user.last_date1>user.last_date2:
                user.last_date2 = datetime.utcnow()
                user.last_ip2 = request.remote_addr
            else:
                user.last_date1 = datetime.utcnow()
                user.last_ip1 = request.remote_addr
            db.session.add(user)
            db.session.commit()
            
    flash(message, category=status)
    return redirect(url_for("index"))

@accounts.route('/list')
@verify_login
def list_all():
    basic = dict()
    user_no = Account.query.filter_by(id=session['user_id']).first().user_no
    basic['account'] = _user_basic_info()
    staff = _query_user_amount(0)
    manager = _query_user_amount(1)
    basic['admin'] = dict(staff=staff, manager=manager)
    account = dict()
    return render_template('account-list.html', basic=basic, account=account)

@accounts.route("/create")
@verify_login
def create():
    return session['status']

@accounts.route("/logout")
def logout():
    session["user_id"] = None
    session["user_no"] = None
    session["time"] = None
    flash('注销成功！')
    return redirect(url_for('accounts.login'))
    
# query the amount of pid type
def _query_user_amount(pid):
    user = Account.query.filter_by(privilege=int(pid)).all()
    return len(user) if user else 0

# query login user basic info
def _user_basic_info():
    user_id = session['user_id']
    info=dict()
    user = Account.query.filter_by(id=user_id).first()
    if user:
        info=dict()
        info['user_no'] = user.user_no
        info['place'] = user.place.place
        if user.last_date1>=user.last_date2:
            info['last_date'] = user.last_date1
            info['last_ip'] = user.last_ip1
        else:
            info['last_date'] = user.last_date2
            info['last_ip'] = user.last_ip2
        return info
    return None
