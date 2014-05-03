from datetime import datetime

from sqlalchemy import and_

from WMS.models import db

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, size=None, amount=None, \
                 item_id=None, place_id=None):
        if size and amount>=0 and item_id and place_id:
            self.size = size
            self.amount = amount
            self.item_id = item_id
            self.place_id = place_id
        else:
            raise ValueError

    def __repr__(self):
        return '{ Storage Object: %s , %s , %s , %s }' % \
               (self.size, self.amount, \
                self.item_id, self.place_id)

    @staticmethod
    def add_batch(data):
        '''
        update storage bashly

        @param
            data: list
                list of item to be update
                data format:
                items:list
                    item: dict
                        key => Value
                        item_id => item_id
                        place_id => place_id
                        size => size
                        amount => amount
        '''
        if data == None:
            raise ValueError
        for detail in data:
            item_id = detail['item_id']
            place_id = detail['place_id']
            size = detail['size']
            amount = detail['amount']
            storage = Storage.query.filter(and_(Storage.item_id==item_id, 
                                                Storage.place_id==place_id,
                                                Storage.size==size)).first()
            if storage==None:
                storage = Storage(size, 0, item_id, place_id)
            storage.amount = storage.amount + amount
            db.session.add(storage)
        db.session.commit()