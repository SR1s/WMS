from WMS.config.database import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, \
                                MYSQL_PASS, MYSQL_DB


DEBUG = True
SECRET_KEY = 'yguesswhatkeyitis'
CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI  =  'mysql://%s:%s@%s:%s/%s' % \
                            (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, \
                             MYSQL_PORT, MYSQL_DB)