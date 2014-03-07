from WMS.models import db
from datetime import datetime 

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(255), db.ForeignKey('order.order_no'))
    date = db.Column(db.DateTime,default=datetime.utcnow)
    details = db.relationship("IncomeDetail", backref="order", lazy='dynamic')