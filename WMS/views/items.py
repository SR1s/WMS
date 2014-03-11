from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Item
from WMS.views import verify_login


items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def all_items():
    items_raw = Item.query.order_by(Item.number.desc()).all()
    items = dict()
    for item_raw in items_raw:
        if items.has_key(item_raw.number):
            item = items.get(item_raw.number)
            if item['info'].last_update < item_raw.last_update:
                item['info'].last_update = item_raw.last_update
        else:
            item = items[item_raw.number] = dict()
            item['info'] = item_raw
        item[item_raw.size] = item.get(item_raw.size, 0) + item_raw.amount

    return render_template("item-list.html", items=items)
