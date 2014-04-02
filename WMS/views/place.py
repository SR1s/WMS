#coding: utf8

from flask import Blueprint, render_template, abort, flash, \
                    request, session, redirect, url_for
from WMS.app import db
from WMS.forms.accounts import LoginForm
from WMS.models import Place, Account
from WMS.utils import md5
from WMS.views import verify_login

place = Blueprint('place', __name__)

@place.route('/add', methods=['POST'])
@verify_login
def add():
    place = Place(request.form['place'])
    db.session.add(place)
    db.session.commit()
    return redirect(url_for('accounts.list_all'))