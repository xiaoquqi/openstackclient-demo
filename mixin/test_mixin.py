#!/usr/bin/env python

class BaseClass(object):
    def test1(self):
        print "BaseClass"

class Mixin1(object):
    def test2(self):
        print "Mixin1"

class Mixin2(object):
    def test3(self):
        print "Mixin2"

class MyClass(BaseClass, Mixin1, Mixin2):
    pass

my_class = MyClass()
my_class.test1()
my_class.test2()
my_class.test3()
