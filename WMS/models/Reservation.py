from WMS.models import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    address = db.Column(db.String(255))
    note = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    # 0: not finish ; 1: finish; -1: can't finish, also means delete
    status = db.Column(db.Integer, default=0)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __init__(self, name, contact, address, item_id, amount, note=None):
        self.name = name
        self.contact = contact
        self.address = address
        self.item_id = item_id
        self.amount = amount
        if note:
        	self.note = note

    def __repr__(self):
        return "{{-- Reservation Object: %s --}}" % self.name