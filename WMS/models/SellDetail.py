from datetime import datetime

from sqlalchemy import and_

from WMS.models import db
from WMS.views import sort_cal_all

class SellDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255))
    amount = db.Column(db.Integer, default=0)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    sell_id = db.Column(db.Integer, db.ForeignKey('sell.id'))

    def __init__(self, 
    	         item_id=None, 
    	         sell_id=None,   
    	         size=None,
    	         amount=None):
    	if item_id and sell_id and size and amount:
    		self.item_id = item_id
    		self.sell_id = sell_id
    		self.size = size
    		self.amount = amount
    	else:
    		raise ValueError

    def to_dict(self, extra=False):
        temp = dict(
                    id=self.id,
                    item_id=self.item_id,
                    sell_id=self.sell_id,
                    size=self.size,
                    amount=self.amount,
                    number=self.item.number,
                    description=self.item.description,
                    retail=self.item.retail,
                    whole=self.item.whole,
                    last_update=self.item.last_update,
                    )
        return temp