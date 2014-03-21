#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, session, redirect, url_for
from WMS.models import db   
from WMS.config import app_config

from WMS.views.accounts import accounts
from WMS.views.items import items
from WMS.views.order import order
from WMS.views.income import income

def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(accounts, url_prefix="/accounts")
    app.register_blueprint(items, url_prefix="/items")
    app.register_blueprint(order, url_prefix="/order")
    app.register_blueprint(income, url_prefix="/income")
    app.config.from_object(app_config)
    
    if config:
        app.config.update(config)

    db.init_app(app)
    set_up(app)
    return app

def set_up(app):
    @app.route('/')
    def index():
        if "status" in session and session["status"] == "logined":
            return render_template('status.html')
        else:
            return redirect(url_for("accounts.login"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
