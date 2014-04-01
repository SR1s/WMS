#coding: utf8
from flask import Blueprint, render_template, abort, request, \
                  session, redirect, url_for, flash
from sqlalchemy import and_
from WMS.app import db
from WMS.models import Item, Storage, Place
from WMS.views import verify_login, sort_cal_all

import json

items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def list_all():
    storage = dict()
    storage['items'] = dict()
    place_id = session['place_id']
    for s in Storage.query.filter_by(place_id=place_id).all():
        item = storage['items'].setdefault(s.item.number, dict())
        item['number'] = s.item.number
        item['description'] = s.item.description
        item['last_update'] = str(s.item.last_update.date())
        columns = item.setdefault('columns', list())
        columns.append(dict(size=s.size, amount=s.amount))
    for item in storage['items']:
        c = storage['items'][item]['columns']
        if len(c)<6:
            n = 7-len(c)
            for x in range(0,n):
                c.append(dict(size='-',amount=0))
        storage['items'][item]['sum'] = sort_cal_all(c)
        
    #return json.dumps(storage)
    basic = dict()
    basic['place'] = Place.query.filter_by(id=place_id).first().place
    basic['info'] = info = dict()
    info['count'] = 0
    info['amount'] = 0
    
    return render_template("item-list.html", storage=storage, basic=basic)

@items.route('/sell')
def sell():
    return render_template("sell-create.html")

@items.route('/sell', methods=['POST'])
def perform_create():
    details = json.loads(request.form['details'])
    item_result = list()
    isOk = True
    store = list()
    for (key, detail) in details.items():
        item = Item.query.filter_by(number=detail['number']).first()
        if item:
            place_id = session['place_id']
            for c in detail['columns']:
                have = Storage.query.filter(and_(Storage.item_id==item.id,Storage.place_id==place_id, Storage.size==c['size'])).first().amount
                rest = have - int(c['amount'])
                if rest<0:
                    isOk=False
                    flash('编号:%s 尺寸:%s的货物库存不足，剩余:%s，需要:%s' %\
                          (detail['number'], c['size'], have, c['amount']))
                store.append(dict(item_id=item.id, amount=rest, size=c['size']))
        else:
            isOk = False
            flash('不存在编号%s的货物' % detail['number'], category='error')
        #return json.dumps(store)
    if isOk:
        for s in store:
            change = Storage.query.filter(and_(Storage.item_id==s['item_id'],\
                                               Storage.size==s['size'], \
                                               Storage.place_id==session['place_id'])).first()
            change.amount=s['amount']
            db.session.add(change)
        db.session.commit()
        flash('出货成功', 'normal')
    return redirect(url_for('items.list_all'))