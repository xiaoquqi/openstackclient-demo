#!/usr/bin/env python

from sqlalchemy.orm import sessionmaker

from connection import engine
from models import Department, Employee

session = sessionmaker()
session.configure(bind=engine)

s = session()

# Query all records

for e in s.query(Employee).all():
    print "Employee name is", e.name

print "-" * 30

# Condition Query
employees = s.query(Employee).join(Employee.department).filter(
        Employee.name.startswith('R'), Department.name == 'Dev').all()

for e in employees:
    print "Employee: %s" % e.name
    print "Department: %s" % e.department.name
