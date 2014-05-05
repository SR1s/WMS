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