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
        if session["status"] == "logined" and session['time']:
            return func()
        else:
            return redirect(url_for('accounts.login'))
    return wrappper