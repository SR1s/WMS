from WMS.models import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255), unique=True)
    person = db.relationship("Account", backref="place", lazy='dynamic')
    storage = db.relationship("Storage", backref="place", lazy='dynamic')
    order = db.relationship("Order", backref="place", lazy='dynamic')
    sell = db.relationship("Sell", backref="place", lazy='dynamic')

    def __init__(self, place=None):
        if place:
        	self.place = place
        else:
            raise ValueError

    def __repr__(self):
        return '{ Place Object: %s , %s }' % \
               (self.id, self.place)