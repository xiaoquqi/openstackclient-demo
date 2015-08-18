#!/usr/bin/env python

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('departments.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department,
        backref=backref('employees',
                         uselist=True,
                         cascade='delete,all'))


from sqlalchemy import create_engine
engine = create_engine('sqlite:///demo.sqlite', echo=True)

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

def all_employees(s):
    print "------------------------------------------"
    print "current employees"
    for e in s.query(Employee).all():
        print e.name
    print "------------------------------------------"


# create new record
dep = Department(name="Dev")
emp1 = Employee(name="Ray", department=dep)
emp2 = Employee(name="Wendy", department=dep)
s = session()
s.add(dep)
s.add(emp1)
s.add(emp2)
s.commit()
print "Add a new dep %s and new employee %s" % (dep.name, emp1.name)
all_employees(s)

print "Removing dep %s" % (dep.name)
#s.delete(dep)
all_employees(s)

employees = s.query(Employee).join(Employee.department).filter(
        Employee.name.startswith('R'), Department.name == 'Dev').all()

for e in employees:
    print "Employee: %s" % e.name
    print "Department: %s" % e.department.name
