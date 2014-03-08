from WMS import app
from WMS import db

with app.test_request_context():
    db.drop_all()