from flask import Blueprint, render_template, abort, request, session
from WMS.app import db
from WMS.models import Item
from WMS.views import verify_login


items = Blueprint('items', __name__)

@items.route("/all")
@verify_login
def all_items():
    items = Items.query.all()
    return str(items)
