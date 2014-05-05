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
from WMS.views.place import place
from WMS.views.reservation import reservation
from WMS.views.sell import sell
from WMS.views import verify_login

def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(accounts, url_prefix="/accounts")
    app.register_blueprint(items, url_prefix="/items")
    app.register_blueprint(order, url_prefix="/order")
    app.register_blueprint(income, url_prefix="/income")
    app.register_blueprint(place, url_prefix="/place")
    app.register_blueprint(reservation, url_prefix="/reservation")
    app.register_blueprint(sell, url_prefix="/sell")
    app.config.from_object(app_config)
    
    if config:
        app.config.update(config)

    db.init_app(app)
    set_up(app)
    return app

def set_up(app):
    @app.route('/')
    @verify_login
    def index():
        return redirect(url_for("items.list_all"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
