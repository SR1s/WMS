from flask import Blueprint, render_template, abort, request, \
                  session, redirect, url_for, flash 
from WMS.app import db
from WMS.models import Item
from WMS.views import verify_login

import json


items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def list_all():
    items_raw = Item.query.order_by(Item.number.desc()).all()
    return render_template("item-list.html", items=items_raw)

@items.route('/sell')
def create():
    return render_template("sell-create.html")

@items.route('/sell', methods=['POST'])
def perform_create():
    #no = request.form['sell_no']
    details = json.loads(request.form['details'])
    item_result = list()
    isOk = True
    for detail in details:
        item = Item.query.filter_by(number=detail['number']).first()
        if item:
            item = dict(id=item.id, \
                        size1=item.size1, amount1=item.amount1, \
                        size2=item.size2, amount2=item.amount2, \
                        size3=item.size3, amount3=item.amount3, \
                        size4=item.size4, amount4=item.amount4, \
                        size5=item.size5, amount5=item.amount5, \
                        size6=item.size6, amount6=item.amount6 )
            i,j = 1,1
            for i in range(1,7):
                for j in range(1,7):
                    if item["size"+str(i)] == detail["size"+str(j)]:
                        item["amount"+str(i)] = int(item["amount"+str(i)]) - int(detail["amount"+str(j)])
                        item_result.append(item)
        else:
            isOk = False
            flash('item: %s not exist' % detail['number'], category='error')
    if isOk:
        for item in item_result:
            item_result = Item.query.filter_by(id=item['id']).first()
            item_result.amount1 = item['amount1']
            item_result.amount2 = item['amount2']
            item_result.amount3 = item['amount3']
            item_result.amount4 = item['amount4']
            item_result.amount5 = item['amount5']
            item_result.amount6 = item['amount6']
            db.session.add(item_result)
            db.session.commit()
        flash('successfully sell', 'normal')
    return redirect(url_for('items.list_all'))