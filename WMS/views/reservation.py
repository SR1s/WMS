#coding: utf8
from flask import Blueprint, render_template, abort, request, session, \
                  redirect, url_for, flash
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
    reservations = Reservation.query.filter_by(status=0).all()
    basic=dict()
    basic['all'] = len(reservations)
    return render_template('reservation-list.html', \
                            reservations = reservations, \
                            basic=basic)

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

@reservation.route('/done')
@verify_login
def done():
    reser_id = request.args.get('id')
    reservation = Reservation.query.filter_by(id=reser_id).first()
    reservation.status = 1
    db.session.add(reservation)
    db.session.commit()
    flash('预约已处理')
    return redirect(url_for('reservation.list_all'))

@reservation.route('/delete')
@verify_login
def delete():
    reser_id = request.args.get('id')
    reservation = Reservation.query.filter_by(id=reser_id).first()
    reservation.status = -1
    db.session.add(reservation)
    db.session.commit()
    flash('预约已删除')
    return redirect(url_for('reservation.list_all'))
