#coding: utf8
from datetime import datetime
import json

from flask import (Blueprint, render_template, abort, request, 
                   session, redirect, url_for, flash )
from sqlalchemy import and_

from WMS.app import db
from WMS.models import Item, Storage, Place
from WMS.models.Sell import Sell
from WMS.utils import Log
from WMS.views import verify_login, sort_cal_all

sell = Blueprint('sell', __name__)

@sell.route('/create')
@verify_login
def create():
    return render_template("sell-create.html")

@sell.route('/create', methods=['POST'])
def perform_create():
    place_id = session['place_id']
    date = request.form.get('date', datetime.utcnow())
    details = json.loads(request.form['details'])

    valid_data=dict()
    # validation Start-->
    is_data_valid = True
    for (number, detail) in details.items():
        item = Item.query.filter_by(number=number.upper()).first()
        if item == None:
            flash('Item %s not exist' % number, 'error')
            is_data_valid = False
            continue
        item_id = item.id
        for (size, amount) in detail['columns'].items():
            stor = Storage.query.filter(and_(Storage.place_id== place_id,
                                             Storage.item_id == item_id,
                                             Storage.size    == size)).first()
            if stor and stor.amount >= amount:
                valid_detail = valid_data.setdefault(number, dict())
                valid_detail.setdefault('item_id', item_id)
                columns = valid_detail.setdefault('columns', dict())
                columns[size] = amount
            else:
                flash('did not have enough storage for item: %s,size %s' % \
                      (number, size))
                is_data_valid = False
    if is_data_valid:
        pass
    else:
        return redirect(url_for('sell.create'))

    # <-- validation End

    # assembling data
    data = dict()
    data['place_id'] = place_id
    data['date'] = date
    data['items'] = valid_data
    Sell.create_sell_record(data)

    return redirect(url_for('items.list_all'))