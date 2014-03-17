from flask import session, render_template, url_for, redirect
import functools

def verify_login(func):
    @functools.wraps(func)
    def wrappper():
        if session["status"] == "logined":
            return func()
        else:
            return redirect(url_for('accounts.login'))
    return wrappper