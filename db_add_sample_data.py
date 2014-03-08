#!/usr/bin/python

from WMS import app
from WMS import db
from tests.set_test_data import set_up_data

with app.test_request_context():
    set_up_data(db)