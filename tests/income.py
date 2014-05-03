# coding: utf-8
import json
import os
import tempfile
import unittest

from WMS import create_app, db
from WMS.models.Order import Order
from WMS.utils import readXls

from tests.set_test_data import set_up_data


class IncomeTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        config = {
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': "sqlite:////" + self.db_path,
        }
        app = create_app(config)
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:////" + self.db_path
        app.config['TESTING'] = True
        app.config["CSRF_ENABLED"] = False
        self.app = app
        self.client = app.test_client()
        with app.test_request_context():
            db.create_all(app = app)
            set_up_data(db)
            
        print "\n"

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_remain(self):
    	data = readXls('temp.xls', 0)
    	data['place_id'] = 3
        with self.app.test_request_context():
    		order_id = Order.create_an_order(data)
    		result = Order.query_order(order_id)
    		remain = Order.query_order_remain(order_id)
    		self.assertEqual(json.dumps(result), json.dumps(remain))
