#coding: utf8
import json

from flask import Blueprint, render_template, abort, flash, \
                    request, session, redirect, url_for
from WMS.app import db
from WMS.forms.accounts import LoginForm
from WMS.models import Place, Account
from WMS.utils import md5
from WMS.views import verify_login

from sqlalchemy import and_

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
        user = Account.query.filter(and_(Account.user_no==user_no, \
                                         Account.user_ps==user_ps, \
                                         Account.privilege>-1)).first()
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
    place = len(Place.query.all())
    basic['admin'] = dict(staff=staff, manager=manager, place=place)
    accounts = Account.query.filter(Account.privilege>-2).all()
    accounts = [_user_basic_info(a.id)
                for a in accounts]
    places = Place.query.all()
    return render_template('account-list.html', \
                            basic=basic, accounts=accounts, places=places)

@accounts.route('/disable', methods=['POST'])
@verify_login
def disable():
    user_no = request.form['user_no']
    account = Account.query.filter(and_(Account.user_no==user_no, \
                                        Account.privilege>=0)).first()
    if account:
        account.privilege=-1
        db.session.add(account)
        db.session.commit()
        flash('账户%s已禁用' % user_no)
        return redirect(url_for('accounts.list_all'))
    flash('操作无效')
    return redirect(url_for('accounts.list_all'))

@accounts.route('/delete', methods=['POST'])
@verify_login
def delete():
    user_no = request.form['user_no']
    account = Account.query.filter(and_(Account.user_no==user_no, \
                                        Account.privilege>=-1)).first()
    if account:
        account.privilege=-2
        db.session.add(account)
        db.session.commit()
        flash('账户%s已删除' % user_no)
        return redirect(url_for('accounts.list_all'))
    flash('操作无效')
    return redirect(url_for('accounts.list_all'))

@accounts.route('/alter', methods=['POST'])
@verify_login
def alter():
    user_no = request.form['user_no']
    place = request.form['place']
    role = request.form['role']
    user = Account.query.filter(and_(Account.user_no==user_no, \
                                     Account.privilege>-1)).first()
    if user:
        user.privilege = role
        user.place_id = place
        db.session.add(user)
        db.session.commit()
        flash('更改用户%s信息成功!' % user_no, 'normal')
    else:
        flash('操作失败', 'error')
    return redirect(url_for('accounts.list_all'))
    

@accounts.route("/create", methods=['POST'])
@verify_login
def create():
    user_no = request.form['user_no']
    user_ps = request.form['user_ps']
    role = request.form['role']
    place = request.form['place']
    if Account.query.filter(and_(Account.user_no==user_no, \
                                 Account.privilege!=-2)).first():
        flash('工号：%s的帐号已经存在' % user_no, 'error')
    else:
        account = Account(user_no=user_no, user_ps=md5(user_ps),
                          privilege=role, place_id=place)
        db.session.add(account)
        db.session.commit()
    return redirect(url_for('accounts.list_all'))

@accounts.route("/logout")
def logout():
    session["user_id"] = None0
    session["user_no"] = None
    session["time"] = None
    flash('注销成功！')
    return redirect(url_for('accounts.login'))
    
# query the amount of pid type
def _query_user_amount(pid):
    user = Account.query.filter_by(privilege=int(pid)).all()
    return len(user) if user else 0

# query login user basic info
def _user_basic_info(user_id=None):
    if user_id==None:
        user_id = session['user_id']
    info=dict()
    user = Account.query.filter_by(id=user_id).first()
    if user:
        info=dict()
        info['user_no'] = user.user_no
        info['place'] = user.place.place
        info['pid'] = user.place.id
        info['role'] = _user_role(user.privilege)
        info['rid'] = user.privilege
        if user.last_date1>=user.last_date2:
            info['last_date'] = user.last_date1
            info['last_ip'] = user.last_ip1
        else:
            info['last_date'] = user.last_date2
            info['last_ip'] = user.last_ip2
        return info
    return None
    
def _user_role(role_id):
    roles = {'0':'普通员工', '1':'经理', \
             '-1': '已禁用', '-2': '已删除', \
             '255':'管理员'}
    if str(role_id) in roles:
        return roles[str(role_id)]
    else:
        return '未定义身份'
