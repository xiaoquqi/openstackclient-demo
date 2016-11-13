#!/usr/bin/env python


from sqlalchemy.orm import sessionmaker

from connection import engine
from models import Base

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
