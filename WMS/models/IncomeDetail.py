from WMS.models import db

class IncomeDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    income_id = db.Column(db.Integer, db.ForeignKey('income.id'))

    def __init__(self, item_id=None, income_id=None, \
                 size=None, amount=None):
        if item_id and income_id and size and amount:
            self.item_id = item_id
            self.income_id = income_id
            self.size = size
            self.amount = amount
        else:
            raise ValueError

    def __repr__(self):
        return '{ IncomeDetail Object: %s , %s , %s , %s }' % \
                (self.item_id, self.income_id, self.size, self.amount)