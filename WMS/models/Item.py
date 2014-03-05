from WMS.models import db
from datetime import datetime 

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    size = db.Column(db.String(255))
    description = db.Column(db.String(255))
    place = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    last_upadte = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, number, size, description, amount):
        self.number = number
        self.size = size
        self.description = description
        self.amount = amount

    def __repr__(self):
        return "<Item: \n    number: %s \n    size: %s \n    amount: %s \n>" % \
                (self.number, self.size, self.amount)