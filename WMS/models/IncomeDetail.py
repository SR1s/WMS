from WMS.models import db

class IncomeDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    size = db.Column(db.String(255))
    description = db.Column(db.String(255))
    place = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    retail_price = db.Column(db.Float)
    whole_sell_price = db.Column(db.Float)
    total = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __init__(self, number, size, description, amount):
        self.number = number
        self.size = size
        self.description = description
        self.amount = amount

    def __repr__(self):
        return "<IncomeDetail: \n    number: %s \n    size: %s \n    amount: %s \n>" % \
                (self.number, self.size, self.amount)