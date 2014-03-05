#encoding=utf-8
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask
from WMS.models import db
from WMS.models.Income import Income

from WMS.config.database import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, \
                                MYSQL_PASS, MYSQL_DB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % \
                                        (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, \
                                         MYSQL_PORT, MYSQL_DB)
app.debug = True
app.secret_key = 'guesswhatkeyitis'
db.init_app(app)
