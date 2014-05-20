from datetime import datetime
import json

from sqlalchemy import and_

from WMS.models import db
from WMS.models.Item import Item
from WMS.views import sort_cal_all

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

    def to_dict(self, extra=False):
        temp = dict(
                    id=self.id,
                    size=self.size,
                    amount=self.amount,
                    item_id=self.item_id,
                    place_id=self.place_id,
                    number=self.item.number,
                    description=self.item.description,
                    retail=self.item.retail,
                    whole=self.item.whole,
                    last_update=str(self.item.last_update.date()),
                    place=self.place.place,
                    )
        return temp

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

    @staticmethod
    def minus_batch(data):
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
            storage.amount = storage.amount - amount
            db.session.add(storage)
        db.session.commit()

    @staticmethod
    def query_all_storage(raw=False):
        '''
        @date: 14-05-04

        @return: list of all storage, data structure like:
            data: dict
                number => storage: dict
                    'number': String 
                    'description': String
                    'last_update': String
                    'details': list
                        place => detail: dict
                            'place': String
                            'sum': Integer
                            'items': list
                                item['size']
                                item['amount']
        '''
        storages = Storage.query.order_by(Storage.item_id).all()

        if raw:
            return [storage.to_dict() for storage in storages]

        data=dict()
        for storage in storages:
            storage = storage.to_dict()
            item = data.setdefault(storage['number'], dict())
            item.setdefault('number', storage['number'])
            item.setdefault('description', storage['description'])
            item.setdefault('last_update', storage['last_update'])
            details = item.setdefault('details', dict())
            detail = details.setdefault(storage['place'], dict())
            detail.setdefault('place', storage['place'])
            items = detail.setdefault('items', list())
            items.append(dict(size=storage['size'], amount=storage['amount']))
        for (number, storage) in data.items():
            for (place, place_detail) in storage['details'].items():
                items = place_detail['items']
                place_detail['sum'] = sort_cal_all(items)
        return data

    @staticmethod
    def query_storage(place_id=place_id, raw=False):
        '''
        @date: 14-05-04

        @return: list of certain place storage, data structure like:
            data: dict
                number => storage: dict
                    'number': String 
                    'description': String
                    'last_update': String
                    'details': list
                        place => detail: dict
                            'place': String
                            'sum': Integer
                            'items': list
                                item['size']
                                item['amount']
        '''
        storages = Storage.query.filer_by(place_id=place_id).order_by(Storage.item_id).all()

        if raw:
            return [storage.to_dict() for storage in storages]

        data=dict()
        for storage in storages:
            storage = storage.to_dict()
            item = data.setdefault(storage['number'], dict())
            item.setdefault('number', storage['number'])
            item.setdefault('description', storage['description'])
            item.setdefault('last_update', storage['last_update'])
            details = item.setdefault('details', dict())
            detail = details.setdefault(storage['place'], dict())
            detail.setdefault('place', storage['place'])
            items = detail.setdefault('items', list())
            items.append(dict(size=storage['size'], amount=storage['amount']))
        for (number, storage) in data.items():
            for (place, place_detail) in storage['details'].items():
                items = place_detail['items']
                place_detail['sum'] = sort_cal_all(items)
        return data

    @staticmethod
    def query_by_number(number, with_status=False):
        result=dict()
        item = Item.query.filter_by(number=number).first()
        if item:
            result['status']='ok'
            result['status_code']='1'
            result['data'] = dict()
            result['item_info'] = item.to_dict()
            result['item_info']['last_update'] = str(result['item_info']['last_update'].date())
            storages = Storage.query.filter_by(item_id=item.id).all()
            for storage in storages:
                stor_dict = storage.to_dict()
                place_detail = result['data'].setdefault(stor_dict['place'], 
                                                         dict())
                place_detail['place'] = stor_dict['place']
                items = place_detail.setdefault('items', list())
                items.append(dict(size=storage.size, amount=storage.amount))
            result['data'] = result['data'].values()
        else:
            result['status']='error, item no found'
            result['status_code']='0'

        return result