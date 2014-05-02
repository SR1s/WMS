#coding: utf-8

from datetime import datetime

from sqlalchemy import and_

from WMS.models import db
from WMS.models import Income, IncomeDetail
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
            self.no = no
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
    
    def create(self, number=None, date=None, details=None):
        if number==None or details==None:
            raise ValueError
        if date==None:
            date = datetime.utcnow()

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

    # return : dict
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

def chkstatus(status_code):
    if status_code==0:
        return u'尚未到货完毕'
    elif status_code==1:
        return u'到货完毕'
    elif status_code==-1:
        return u'订单已删除'
    return '状态异常'
