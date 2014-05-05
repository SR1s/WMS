from datetime import datetime

from sqlalchemy import and_

from WMS.models import db
from WMS.views import sort_cal_all

class Sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    details = db.relationship("SellDetail", backref="sell", lazy='dynamic')

    def __init__(self, place_id=None, date=None):
        if place_id:
            self.place_id = place_id
        else:
            raise ValueError
        if date:
            self.date = date
        else:
            self.data = datetime.utcnow()

    @staticmethod
    def create_sell_record(data):
        '''
        @param
            data: dict
            data['place_id']: Integer
            data['data']: datetime[Option]
            data['details']: dict
                number => detial:
                          detail['size']
                          detail['amount']
        @return sell_id if success
        '''
        pass