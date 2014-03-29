from flask import Blueprint, render_template, abort, request, \
                  session, redirect, url_for, flash 
from sqlalchemy import and_
from WMS.app import db
from WMS.models import Item, Storage
from WMS.views import verify_login, mycmp, cal_all

import json


items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def list_all():
    storage = dict()
    storage['items'] = dict()
    for s in Storage.query.filter_by(place_id=1).all():
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
        c.sort(mycmp)
        storage['items'][item]['sum'] = cal_all(c)
        
    #return json.dumps(storage)
    return render_template("item-list.html", storage=storage)

@items.route('/sell')
def create():
    return render_template("sell-create.html")

@items.route('/sell', methods=['POST'])
def perform_create():
    details = json.loads(request.form['details'])
    item_result = list()
    isOk = True
    store = list()
    for detail in details:
        item = Item.query.filter_by(number=detail['number']).first()
        if item:
            place_id = session['place_id']
            for c in detail['columns']:
                have = Storage.query.filter(and_(Storage.item_id==item.id,Storage.place_id==place_id, Storage.size==c['size'])).first().amount
                rest = have - int(c['amount'])
                if rest<0:
                    isOk=False
                    flash('Item:%s is not enough.have:%s, require:%s' %\
                          (detail['number'], have, c['amount']))
                store.append(dict(item_id=item.id, amount=rest, size=c['size']))
        else:
            isOk = False
            flash('item: %s not exist' % detail['number'], category='error')
        #return json.dumps(store)
    if isOk:
        for s in store:
            change = Storage.query.filter(and_(Storage.item_id==s['item_id'],\
                                               Storage.size==s['size'], \
                                               Storage.place_id==session['place_id'])).first()
            change.amount=s['amount']
            db.session.add(change)
        db.session.commit()
        flash('successfully sell', 'normal')
    return redirect(url_for('items.list_all'))