#!/usr/bin/python

from WMS import app
from WMS import db
from WMS.models import Place, Account, Item, Order, OrderDetail, Storage

with app.test_request_context():
    print 'droping all tables....'
    db.drop_all()
    print 'all tables dropped.'

    print 'creating tables....'
    db.create_all()
    print 'tables created.'

    print 'set up basic data for system...'
    # add place for administrator
    place = Place(place='-')
    db.session.add(place)
    db.session.commit()

    # add administrator account
    admin = Account(user_no ='admin', 
                    user_ps='admin',
                    place_id=place.id, 
                    privilege=255)
    db.session.add(admin)
    db.session.commit()
    print 'seted up basic data for system done.'
    print 'now you can using the system.'