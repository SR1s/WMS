from WMS.models import db

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255))
    amount = db.Column(db.Integer, default=0)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __init__(self, item_id=None, order_id=None, \
                 size=None, amount=None):
        if item_id and order_id and size and amount:
            self.item_id = item_id
            self.order_id = order_id
            self.size = size
            self.amount = amount
        else:
            raise ValueError

    def __repr__(self):
        return '{ OrderDetail Object: %s , %s , %s , %s }' % \
                (self.item_id, self.order_id, self.size, self.amount)
                
    def to_dict(self, extra=False):
        temp =  dict(
                    size=self.size,
                    amount=self.amount,
                    item_id=self.item_id,
                    number=self.item.number,
                    order_id=self.order_id,
                    )
        if extra:
            temp.setDefault('item', self.item.to_dict())
            temp.setDefault('order', self.order.to_dict())
        return temp
