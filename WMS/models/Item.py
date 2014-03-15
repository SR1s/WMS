from WMS.models import db
from datetime import datetime 

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    description = db.Column(db.String(255))
    size1 = db.Column(db.String(255))
    size2 = db.Column(db.String(255))
    size3 = db.Column(db.String(255))
    size4 = db.Column(db.String(255))
    size5 = db.Column(db.String(255))
    size6 = db.Column(db.String(255))
    amount1 = db.Column(db.Integer)
    amount2 = db.Column(db.Integer)
    amount3 = db.Column(db.Integer)
    amount4 = db.Column(db.Integer)
    amount5 = db.Column(db.Integer)
    amount6 = db.Column(db.Integer)
    place = db.Column(db.Integer, db.ForeignKey('place.id'))
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, number, description, \
                 size1, amount1, size2, amount2, \
                 size3, amount3, size4, amount4, \
                 size5, amount5, size6, amount6, \
                 place, date = None):
        self.number = number
        self.description = description
        self.size1 = size1
        self.size2 = size2
        self.size3 = size3
        self.size4 = size4
        self.size5 = size5
        self.size6 = size6
        self.amount1 = amount1
        self.amount2 = amount2
        self.amount3 = amount3
        self.amount4 = amount4
        self.amount5 = amount5
        self.amount6 = amount6
        self.place = place
        if date:
            self.last_update = date

    def __repr__(self):
        return "{ Number: %s; Description: %s;\n " + \
               "  Place: %s; Date: %s; \n" + \
               "  Size1: %s; Amount1: %s; \n" + \
               "  Size2: %s; Amount2: %s; \n" + \
               "  Size3: %s; Amount3: %s; \n" + \
               "  Size4: %s; Amount4: %s; \n" + \
               "  Size5: %s; Amount5: %s; \n" + \
               "  Size6: %s; Amount6: %s; \n" + \
               "}" % \
               ( self.number, self.description, \
                 self.place, self.last_update, \
                 self.size1, self.amount1, \
                 self.size2, self.amount2, \
                 self.size3, self.amount3, \
                 self.size4, self.amount4, \
                 self.size5, self.amount5, \
                 self.size6, self.amount6, \
                )