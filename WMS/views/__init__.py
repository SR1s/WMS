from flask import session, render_template
import functools

def verify_login(func):
    @functools.wraps(func)
    def wrappper():
        if session["status"]:
            return func()
        else:
            return render_template("404.html"), 404
    return wrappper