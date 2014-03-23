from WMS.models import db
from datetime import datetime 

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    no = db.Column(db.String(255), unique=True)
    # 0: unfinished; 1: finished
    status = db.Column(db.Integer, default=0)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    details = db.relationship("OrderDetail", backref="order", lazy='dynamic')
    incomes = db.relationship("Income", backref="order", lazy='dynamic')

    def __init__(self, no=None, date=None, place_id=None):
        if no and place_id:
            self.no = no
            self.place_id = place_id
            if date:
                self.date = date
        else:
            raise ValueError

    def __repr__(self):
        return '{ Order Object: %s , %s }' % \
                (self.no, self.date)