from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from WMS.models.Account import Account
from WMS.models.Income import Income
from WMS.models.IncomeDetail import IncomeDetail
from WMS.models.Item import Item
from WMS.models.Order import Order
from WMS.models.OrderDetail import OrderDetail
from WMS.models.Place import Place
from WMS.models.Reservation import Reservation
from WMS.models.Storage import Storage

from datetime import datetime

def str2datetime(date_str):
	date_p = date_str.split('/')
	if len(date_p) == 3:
		return datetime(int(date_p[2]),int(date_p[0]),int(date_p[1]))
	else:
		return None