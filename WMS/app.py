#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask, render_template
from WMS.models import db
from WMS.models.Income import Income
from WMS.config import app_config

from WMS.views.accounts import accounts

def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(accounts, url_prefix="/accounts")
    
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(app_config)

    db.init_app(app)
    set_up(app)
    return app

def set_up(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
