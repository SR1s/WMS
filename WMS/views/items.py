from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Item
from WMS.views import verify_login


items = Blueprint('items', __name__)

@items.route("/list")
@verify_login
def all_items():
    items = Item.query.order_by(Item.number).all()
    return str(items)
    return render_template("item-list.html")
