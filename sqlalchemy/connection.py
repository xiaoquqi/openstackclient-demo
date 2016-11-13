#/usr/bin/env python

from sqlalchemy import create_engine

connection = "mysql+pymysql://root:sysadmin@127.0.0.1/" +  \
    "test_sqlalchemy?charset=utf8"
engine = create_engine(connection, echo=True)
