# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)


POSTGRES = {
    'user': 'group2',
    'pw': 'cs373group2',
    'db': 'streamglean_db',
    'host': 'streamglean-rds.cxx60yvk87ey.us-east-2.rds.amazonaws.com',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# SQLALCHEMY_POOL_RECYCLE = 3600

# WTF_CSRF_ENABLED = True
# SECRET_KEY = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'