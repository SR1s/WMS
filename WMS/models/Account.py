from WMS.models import db
from datetime import datetime
from WMS.utils import md5

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_no = db.Column(db.String(255), unique=True)
    user_ps = db.Column(db.String(255))
    privilege = db.Column(db.Integer, default=0)
    default_place = db.Column(db.Integer, db.ForeignKey('place.id'))
    last_login = db.Column(db.DateTime,default=datetime.utcnow)
    last_ip = db.Column(db.String(255))

    def __init__(self, user_no, user_ps, default_place):
        self.user_no = user_no
        self.user_ps = md5(user_ps)
        self.default_place = default_place

    def __repr__(self):
        return "<--- Account Object ---> \n no: %s \n ps: %s" % \
                (self.user_no, self.user_ps)