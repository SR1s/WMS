import os
import unittest
import tempfile
from WMS import create_app, db
from tests.set_test_data import set_up_data

class AccountsTest(unittest.TestCase):
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
        self.app = app.test_client()
        with app.test_request_context():
            db.create_all(app = app)
            set_up_data(db)
            
        print "\n"

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_perform_login(self):
        data = ({'no': "a_shenzhen", 'ps': "a_shenzhen"},
                {'no': "a_guangzhou",'ps': "a_guangzhou"},
                {'no': "a_shanghai", 'ps': "a_shanghai"},
                {'no': "a_hongkong", 'ps': "a_hongkong"})
        for case in data:
            rv = self.app.post('/accounts/login', data=dict(
                user_no=case["no"],
                user_ps=case["ps"]
            ), follow_redirects=True)
            print "test with data: %s " % str(case)
            self.assertTrue('you have log in!' in rv.data)