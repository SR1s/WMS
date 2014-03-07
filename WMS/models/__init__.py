from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from Account import Account
from Income import Income
from IncomeDetail import IncomeDetail
from Item import Item
from Order import Order
from OrderDetail import OrderDetail
from Place import Place