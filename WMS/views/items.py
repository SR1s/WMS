#coding: utf8
import json

from flask import (Blueprint, render_template, abort, request, 
                   session, redirect, url_for, flash )
from sqlalchemy import and_

from WMS.app import db
from WMS.models import Item, Storage, Place
from WMS.views import verify_login, sort_cal_all

items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def list_all():
    storages = Storage.query_all_storage()   
    #return json.dumps(storage, indent=2)
    place_id = session['place_id']
    basic = dict()
    basic['place'] = Place.query.filter_by(id=place_id).first().place
    basic['info'] = info = dict()
    info['count'] = 0
    info['amount'] = 0 
    return render_template("item-list.html", storages=storages, basic=basic)

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
                have = Storage.query.filter(and_(Storage.item_id==item.id, \
                                                 Storage.place_id==place_id, \
                                                 Storage.size==c['size'])).first().amount
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

@items.route('/transfer')
@verify_login
def transfer():
    pass