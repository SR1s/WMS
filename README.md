WMS
===

Warehouse Management System

REQUIRE
===

1. Python 2.7
1. MySQL
1. Flask
1. Flask-SQLAlchemy
1. Flask-WTF
1. xlrd

CONFIG
===

1. app : WMS/config/app_config.py
1. database: WMS/config/database.py

DEPLOY
===

1. fill the database information on config file
1. run db_build.py script to initial database
1. run db_add_sample script to add sample data 
1. run run_test.py script to determine if someting wrong
1. run run_app.py script to start the application
