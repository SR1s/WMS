import os
import unittest
import tempfile
from WMS.app import app, db

class AccountsTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:////" + self.db_path
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.test_request_context():
            db.create_all(app = app)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_login(self):
        rv = self.app.get('/accounts/login')
        self.assertTrue('login form will show here' in rv.data)

    def test_perform_login(self):
        rv = self.app.post('/accounts/login')
        self.assertTrue('you have log in!' in rv.data)