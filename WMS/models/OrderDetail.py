from WMS.models import db

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    description = db.Column(db.String(255))
    size1 = db.Column(db.String(255))
    size2 = db.Column(db.String(255))
    size3 = db.Column(db.String(255))
    size4 = db.Column(db.String(255))
    size5 = db.Column(db.String(255))
    size6 = db.Column(db.String(255))
    amount1 = db.Column(db.Integer)
    amount2 = db.Column(db.Integer)
    amount3 = db.Column(db.Integer)
    amount4 = db.Column(db.Integer)
    amount5 = db.Column(db.Integer)
    amount6 = db.Column(db.Integer)
    place = db.Column(db.String(255))
    retail_price = db.Column(db.Float)
    whole_sell_price = db.Column(db.Float)
    total = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __init__(self, number, description, order_id, \
                 size1, amount1, size2, amount2, \
                 size3, amount3, size4, amount4, \
                 size5, amount5, size6, amount6, \
                 retail, whole, total ):
        self.number = number
        self.description = description
        self.order_id = order_id
        self.size1 = size1
        self.size2 = size2
        self.size3 = size3
        self.size4 = size4
        self.size5 = size5
        self.size6 = size6
        self.amount1 = amount1
        self.amount2 = amount2
        self.amount3 = amount3
        self.amount4 = amount4
        self.amount5 = amount5
        self.amount6 = amount6
        self.retail_price = retail
        self.whole_sell_price = whole
        self.total = total

    def __repr__(self):
        return "{OrderDetail: \n    number: %s \n    size: %s \n    amount: %s \n}" % \
                (self.number, self.size, self.amount)

