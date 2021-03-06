#-*-coding: utf-8
from flask import session, render_template, url_for, redirect, flash
import functools
from datetime import datetime, timedelta

def verify_login(func):
    @functools.wraps(func)
    def wrappper():
        valid_time = timedelta(0, 60*15)
        time = session.get('time', None)
        if time and \
            (datetime.utcnow() - time) < valid_time:
            session['time'] = datetime.utcnow()
        else:
            session['time'] = None
        if session['time']:
            return func()
        else:
            return redirect(url_for('accounts.login'))
    return wrappper

def verify_admin(func):
    @functools.wraps(func)
    def wrappper():
        if session['privilege'] == 255:
            return func()
        else:
            flash('权限不足，无法访问', 'error')
            return redirect(url_for('accounts.login'))
    return wrappper

def mycmp(x, y):
    order1 = dict()
    order1['XS']=0
    order1['S']=1
    order1['M']=2
    order1['L']=3
    order1['XL']=4
    order1['XXL']=5
    order1['-']=6

    order2=dict()
    if order1.get(x['size'], 6)-order1.get(y['size'], 6) != 0:
        return order1[x['size']]-order1[y['size']]
    if order2.get(x['size'], 6)-order2.get(y['size'], 6) != 0:
        return order2[x['size']]-order2[y['size']]
    return cmp(x['size'], y['size'])

def sort_cal_all(c):
    c.sort(mycmp)
    sum = 0
    for k in c:
        sum = sum + k['amount']
    while len(c)<6:
        c.append(dict(size='-', amount=0))
    return sum

def chkstatus(status_code):
    if status_code==0:
        return u'尚未到货完毕'
    elif status_code==1:
        return u'到货完毕'
    elif status_code==-1:
        return u'订单已删除'
    return '状态异常'