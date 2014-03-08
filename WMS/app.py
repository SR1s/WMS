#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask
from WMS.models import db
from WMS.models.Income import Income
from WMS.config import app_config

app = Flask(__name__)
app.config.from_object(app_config)
db.init_app(app)

from WMS.controllers.accounts import accounts

app.register_blueprint(accounts, url_prefix="/accounts")
