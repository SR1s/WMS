from WMS.models import db
from datetime import datetime

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255), unique=True)
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, size=None, amount=None, \
                 item_id=None, place_id=None):
        if size and amount and item_id and place_id:
            self.size = size
            self.amount = amount
            self.item_id = item_id
            self.place_id = place_id
        else:
            raise ValueError

    def __repr__(self):
        return '{ Storage Object: %s , %s , %s , %s }' % \
               (self.size, self.amount, \
                self.item_id, self.place_id)
