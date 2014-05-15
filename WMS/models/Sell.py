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
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    details = db.relationship("SellDetail", backref="sell", lazy='dynamic')

    def __init__(self, place_id=None, account_id=None, date=None):
        if place_id and account_id:
            self.place_id = place_id
            self.account_id = account_id
        else:
            raise ValueError
        if date:
            self.date = date
        else:
            self.data = datetime.utcnow()

    def to_dict(self, extra=False):
        temp = dict(
                    id=self.id,
                    date=str(self.date.date()),
                    place_id=self.place_id,
                    account_id=self.account_id,
                    place=self.place.place,
                    account=self.account.user_no,
                    )
        if extra:
            details = SellDetail.query.filter_by(sell_id=self.id).all()
            temp['amount'] = len(details)
            temp['amount_money'] = 0
            for detail in details:
                temp['amount_money'] += detail.amount * detail.retail
        return temp
    @staticmethod
    def create_sell_record(data):
        '''
        @param
            data: dict
            data['place_id']: Integer
            data['account_id']: Integer
            data['date']: datetime[Option]
            data['items'] : dict
                detail['item_id']: Integer
                detail['retail']: Float
                detail[columns]: dict
                    key => amount: Integer
        @return sell_id if success
        '''
        place_id = data['place_id']
        account_id = data['account_id']
        date = data.get('date', datetime.utcnow())
        sell = Sell(place_id, account_id, date)
        db.session.add(sell)
        db.session.commit()

        sell_id = sell.id
        minus_storages = list()
        for (number, item) in data['items'].items():
            item_id = item['item_id']
            retail = item['retail']
            for (size, amount) in item['columns'].items():
                detail = SellDetail(item_id, sell_id, size, amount, retail)
                storage = dict(
                                item_id=item_id,
                                place_id=place_id,
                                size=size,
                                amount=amount,
                          )
                db.session.add(detail)
                minus_storages.append(storage)
        db.session.commit()

        Storage.minus_batch(minus_storages)
        
        return sell_id