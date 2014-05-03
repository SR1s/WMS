from datetime import datetime 

from WMS.models import db
from WMS.models.IncomeDetail import IncomeDetail
from WMS.models.Storage import Storage

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    details = db.relationship("IncomeDetail", backref="order", lazy='dynamic')

    def __init__(self, order_id, date=None):
        self.order_id = order_id
        if date:
            self.date = date
            
    def __repr__(self):
        return '{ Income Object: %s , %s }' % \
                (self.date, self.order_id)

    def to_dict(self, extra=False):
        '''
        @param
            extra: Boolean
                default False, 
                True to return extra information, like details

        @return object information present in dict format. eg:
            dict['id']: Integer
            dict['date']: String like YYYY-MM-DD
            dict['order']: Integer
        '''
        temp =  dict(
                    id = self.id,
                    date=str(self.date.date()),
                    order_id = self.order_id,
                    )
        if extra:
            temp.setdefault('details', self.details.to_dict())
        return temp

    @staticmethod 
    def create_an_order(data):
        '''
        @date: 2014-05-02

        @param data [dict] eg.
            - require:
                data['order_id']:Integer
                data['place_id']:Integer
                data['details'] : list
                     detail['size']: String [not None and not empty]
                     detail['amount']: Integer [>0]
                     detial['item_id']: Integer
            - optional
                data['date']:datetime

        @return income_id if success
        '''
        if data == None:
            raise ValueError
        date = data.get('date', datetime.utcnow())
        income = Income(data['order_id'], date)
        db.session.add(income)
        db.session.commit()

        income_id = income.id
        place_id = data['place_id']
        for detail in data['details']:
            detail.setdefault('place_id', place_id)
            income_detail = IncomeDetail(
                                detail['item_id'],
                                income_id,
                                detail['size'],
                                detail['amount'],
                            )
            db.session.add(income_detail)
        db.session.commit()
        Storage.add_batch(data['details'])
        return income_id

    @staticmethod
    def query_order_income_total(order_id, raw=False, with_order=False):
        '''
        @status: todo
        @date: 2014-05-03

        @param 
            order_id: Integer

        @return
            if with_order: data: list()
            else: date:dict()
        '''
        pass