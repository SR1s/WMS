from datetime import datetime

from sqlalchemy import and_

from WMS.models import db
from WMS.models.SellDetail import SellDetail
from WMS.models.Storage import Storage
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
            data['date']: datetime[Option]
            data['items'] : dict
                detail['item_id']: Integer
                detail[columns]: dict
                    key => amount: Integer
        @return sell_id if success
        '''
        place_id = data['place_id']
        date = data.get('date', datetime.utcnow())
        sell = Sell(place_id, date)
        db.session.add(sell)
        db.session.commit()

        sell_id = sell.id
        minus_storages = list()
        for (number, item) in data['items'].items():
            item_id = item['item_id']
            for (size, amount) in item['columns'].items():
                detail = SellDetail(item_id, sell_id, size, amount)
                storage = dict(
                                item_id=item_id,
                                place_id=place_id,
                                size=size,
                                amount=amount,
                          )
                minus_storages.append(storage)
            db.session.add(detail)
        db.session.commit()

        Storage.minus_batch(minus_storages)
        
        return sell_id