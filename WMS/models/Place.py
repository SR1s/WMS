from WMS.models import db
from datetime import datetime 

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(255), unique=True)
    person = db.relationship("Account", backref="place", lazy='dynamic')

    def __init__(self, place):
        self.place = place

    def __repr__(self):
        return "<-- Place Object: %s -->" % self.place