#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask, render_template
from WMS.models import db
from WMS.models.Income import Income
from WMS.config import app_config

from WMS.views.accounts import accounts
from WMS.views.items import items

def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(accounts, url_prefix="/accounts")
    app.register_blueprint(items, url_prefix="/items")
    app.config.from_object(app_config)
    
    if config:
        app.config.update(config)

    db.init_app(app)
    set_up(app)
    return app

def set_up(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
