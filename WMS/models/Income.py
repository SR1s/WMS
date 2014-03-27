from WMS.models import db
from datetime import datetime 

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    details = db.relationship("IncomeDetail", backref="order", lazy='dynamic')

    def __init__(self, order_id, date=None):
        self.order_id = order_id
        if date:
            self.date = date
            
    def __repr__(self):
        return '{ Income Object: %s , %s }' % \
                (self.date, self.order_id)