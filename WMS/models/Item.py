from WMS.models import db
from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    retail = db.Column(db.Float)
    whole = db.Column(db.Float)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    storage = db.relationship("Storage", backref="item", lazy='dynamic')
    order_details = db.relationship("OrderDetail", backref="item", lazy='dynamic')
    income_details = db.relationship("IncomeDetail", backref="item", lazy='dynamic')
    reservations = db.relationship("Reservation", backref="item", lazy='dynamic')

    def __init__(self, number=None, description=None, \
                 last_update=None, retail = None, whole = None):
        if number and description != None:
            self.number = number
            self.description = description
            if last_update:
                self.last_update = last_update
            if retail:
                self.retail = retail
            if whole:
                self.whole = whole
        else:
            raise ValueError

    def __repr__(self):
        return '{ Item Object: %s , %s , %s }' % \
               (self.number, self.description, self.last_update)

    def to_dict(self, extra=False):
        temp = dict(
                    id=self.id,
                    number=self.number,
                    description=self.description,
                    retail=retail,
                    whole=whole,
                    last_update=last_update,
                    )
        return temp