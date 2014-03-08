#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask, render_template
from WMS.models import db
from WMS.models.Income import Income
from WMS.config import app_config

app = Flask(__name__)
app.config.from_object(app_config)
db.init_app(app)

from WMS.views.accounts import accounts

app.register_blueprint(accounts, url_prefix="/accounts")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
