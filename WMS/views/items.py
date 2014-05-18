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
    info['count'] = len(Item.query.all())
    info['amount'] = 0 
    for storage in Storage.query.all():
        info['amount'] += storage.amount
    for number, storage in storages.items():
        storage['details']=storage['details'].values()            
    items_json = json.dumps(storages.values(), indent=2)
    return render_template("item-list.html", 
                           storages=storages, 
                           basic=basic,
                           items_json=items_json)

@items.route('/transfer')
@verify_login
def transfer():
    pass