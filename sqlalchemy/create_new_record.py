#!/usr/bin/env python

from sqlalchemy.orm import sessionmaker

from connection import engine
from models import Department, Employee

session = sessionmaker()
session.configure(bind=engine)

dep = Department(name="Dev")
emp1 = Employee(name="Ray", department=dep)
emp2 = Employee(name="Wendy", department=dep)

s = session()
s.add(dep)
s.add(emp1)
s.add(emp2)
s.commit()
