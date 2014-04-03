from datetime import datetime
from WMS.models import db
from WMS.utils import md5

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_no = db.Column(db.String(255), unique=True)
    user_ps = db.Column(db.String(255))
    # 0: staff ; 1: manager; 255: administrator; -1: disabled; -2; deleted
    privilege = db.Column(db.Integer, default=0)
    last_date1 = db.Column(db.DateTime,default=datetime.utcnow)
    last_date2 = db.Column(db.DateTime,default=datetime.utcnow)
    last_ip1 = db.Column(db.String(255))
    last_ip2 = db.Column(db.String(255))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, user_no=None, user_ps=None,
                 privilege=None, place_id=None):
        if user_no and user_ps and place_id:
            self.user_no = user_no
            self.user_ps = md5(user_ps)
            self.place_id = place_id
            if privilege:
                self.privilege = privilege
        else:
            raise ValueError

    def __repr__(self):
        return '{ Account Object: %s , %s , %s , %s }' % \
                (self.user_no, self.user_ps, \
                 self.privilege, self.place_id)