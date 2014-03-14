from WMS.models import db
from datetime import datetime 

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(255), unique=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    details = db.relationship("OrderDetail", backref="order", lazy='dynamic')

    def __init__(self, order_no, date=None):
        self.order_no = order_no
        if date :
            self.date = date

    def __repr__(self):
        return "[Order no: %s \n Date : %s \n]" % \
                (self.order_no, self.date)