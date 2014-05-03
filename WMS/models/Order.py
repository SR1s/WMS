#coding: utf-8

from datetime import datetime

from sqlalchemy import and_

from WMS.models import db
from WMS.models import Income, IncomeDetail, Item
from WMS.models.OrderDetail import OrderDetail
from WMS.views import sort_cal_all

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    no = db.Column(db.String(255), unique=True)
    # 0: unfinished; 1: finished
    status = db.Column(db.Integer, default=0)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    details = db.relationship("OrderDetail", backref="order", lazy='dynamic')
    incomes = db.relationship("Income", backref="order", lazy='dynamic')

    def __init__(self, no=None, date=None, place_id=None):
        if no and place_id:
            self.no = no.upper()
            self.place_id = place_id
            if date:
                self.date = date
        else:
            raise ValueError

    def __repr__(self):
        return '{ Order Object: %s , %s }' % \
                (self.no, self.date)
                
    def to_dict(self, extra=False):
        temp =  dict(
                    number = self.no,
                    date=str(self.date.date()),
                    status = chkstatus(self.status),
                    status_code = self.status,
                    id = self.id,
                    place_id = self.place_id,
                    )
        if extra:
            temp.setDefault('place', self.place.to_dict())
        return temp
    
    '''
    @param
        order_id: Integer
            id of order
        raw: Boolean
            return list of data which's structure close to database if set to true;
            else return dict of data which structure close to front end.
            default set to Flase.
        with_order: Boolean
             if set to True, will return with order's information.
             default set to Flase.

    @return
        if raw is true and with_order is False:
            data: list()
                IncomeDetail.to_dict()
    '''
    @staticmethod    
    def query_order_remain(order_id, raw=False, with_order=False):
        order = Order.query.filter_by(id=order_id).first()
        if order == None:
            raise ValueError
        
        incomes = Income.query.filter_by(order_id=order_id).all()
        or_details = OrderDetail.query.filter_by(order_id=order_id).all()
        
        for d in or_details:
            for i in incomes:
                income_id = i.id
                item_id = d.item_id
                size = d.size
                income_item = IncomeDetail.query.filter(and_(
                                    IncomeDetail.income_id == income_id,
                                    IncomeDetail.item_id   == item_id,
                                    IncomeDetail.size      == size,
                                )).first()
                if income_item:
                    d.amount -= income_item.amount
        if raw:
            if with_order:
                results = order.to_dict()
                results['details'] = [d.to_dict() for d in or_details]
            else:
                results = [d.to_dict() for d in or_details]
            return results

        results = dict()
        for d in or_details:
            detail = results.setdefault(d.item.number, dict())
            detail['number'] = d.item.number
            detail['description'] = d.item.description
            columns = detail.setdefault('columns', list())
            columns.append(dict(size=d.size, amount=d.amount))
        for (k, v) in results.items():
            v['sum']=sort_cal_all(v['columns'])
        if with_order:
            order = order.to_dict()
            order['details'] = results
            results = order
        return results 

    '''
    @param 
        order_id: Integer
        raw: Boolean
            default to False, same as query_order_remain
        with_order: Boolean
            default to False, same as query_order_remain
    '''
    @staticmethod    
    def query_order(order_id, raw=False, with_order=False):
        order = Order.query.filter_by(id=order_id).first()
        if order == None:
            raise ValueError

        or_details = OrderDetail.query.filter_by(order_id=order_id).all()
        
        if raw:
            if with_order:
                results = order.to_dict()
                results['details'] = [d.to_dict() for d in or_details]
            else:
                results = [d.to_dict() for d in or_details]
            return results

        results = dict()
        for d in or_details:
            detail = results.setdefault(d.item.number, dict())
            detail['number'] = d.item.number
            detail['description'] = d.item.description
            columns = detail.setdefault('columns', list())
            columns.append(dict(size=d.size, amount=d.amount))
        for (k, v) in results.items():
            v['sum']=sort_cal_all(v['columns'])
        if with_order:
            order = order.to_dict()
            order['details'] = results
            results = order
        return results


    '''
    @param data [dict] eg.
        - require:
            data['order_no']:String[unique]
            data['place_id']:Integer
            data['items'] : dict
                 detial['number']: String[upper]
                 detial['description']: String
                 detial['retail']: Float
                 detial['whole']: Float
                 detial[columns]: dict
                    key => amount: Integer
        - optional
            data['date']:datetime

    @return order_id if success
    '''
    @staticmethod
    def create_an_order(data):
        number = data['order_no']
        place_id = data['place_id']
        date = data.get('date', datetime.utcnow())
        order = Order(number, date, place_id)
        db.session.add(order)
        db.session.commit()

        order_id = order.id
        for (number, det) in data['items'].items():
            item = Item.query.filter_by(number=det['number'].upper()).first()
            if item == None:
                number = det['number']
                description = det['description']
                item = Item(number, description)
            item.retail = det.get('retail', 0)
            item.whole = det.get('whole', 0)
            item.last_update = date
            db.session.add(item)
            db.session.commit()
            item_id = item.id
            for (size, amount) in det['columns'].items():
                detail = OrderDetail(item_id, order_id, size, amount)
                db.session.add(detail)
            db.session.commit()
        return order_id

def chkstatus(status_code):
    if status_code==0:
        return u'尚未到货完毕'
    elif status_code==1:
        return u'到货完毕'
    elif status_code==-1:
        return u'订单已删除'
    return '状态异常'
