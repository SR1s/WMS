#coding: utf8
import json

from flask import (Blueprint, render_template, abort, request, 
                   session, redirect, url_for, flash )
from sqlalchemy import and_

from WMS.app import db
from WMS.models import Item, Storage, Place
from WMS.views import verify_login, sort_cal_all

sell = Blueprint('sell', __name__)

@sell.route('/create')
@verify_login
def create():
	pass