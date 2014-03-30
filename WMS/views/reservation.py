#coding: utf8
from flask import Blueprint, render_template, abort, request, session, \
                  redirect, url_for
from WMS.app import db
from WMS.models import Reservation, Item
from WMS.views import verify_login

reservation = Blueprint('reservation', __name__)

@reservation.route('/create')
@verify_login
def create():
    items = Item.query.all()
    return render_template('reservation-create.html', items=items)

@reservation.route('/list')
@verify_login
def list_all():
    reservations = Reservation.query.all()
    return render_template('reservation-list.html', reservations = reservations)

@reservation.route('/create', methods=['POST'])
@verify_login
def perform_create():
    name = request.form['name']
    contact = request.form['contact']
    address = request.form['address']
    note = request.form['note']
    item_id = request.form['item_id']
    amount = request.form['amount']
    reservation = Reservation(name, contact, address, item_id, amount, note=note)
    db.session.add(reservation)
    db.session.commit()
    return redirect(url_for('reservation.list_all'))