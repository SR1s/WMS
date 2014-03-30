from flask import session, render_template, url_for, redirect
import functools
from datetime import datetime, timedelta

def verify_login(func):
    @functools.wraps(func)
    def wrappper():
    	valid_time = timedelta(0, 60*15)
    	time = session['time']
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

def mycmp(x, y):
    order1 = dict()
    order1['XS']=0
    order1['S']=1
    order1['M']=2
    order1['L']=3
    order1['XL']=4
    order1['XXL']=5
    if order1[x['size']]-order1[y['size']] != 0:
        return order1[x['size']]-order1[y['size']]
    if order2[x['size']]-order2[y['size']] != 0:
        return order2[x['size']]-order2[y['size']]
    return cmp(x['size'], y['size'])

def cal_all(c):
    sum = 0
    for k in c:
        sum = sum + k['amount']
    return sum

def chkstatus(status_code):
    if status_code==0:
        return 'UnFinish'
    elif status_code==1:
        return 'Finished'
    elif status_code==-1:
        return 'Deleted'
    return 'Unknow Status'