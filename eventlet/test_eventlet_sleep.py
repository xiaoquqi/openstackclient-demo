#!/usr/bin/env python

import eventlet
import time

# turn off thread patching to enable the remote debugger
eventlet.monkey_patch(os=False, thread=False)

sleep_times = [5, 1, 10]

def will_sleep(second):
    print "I will sleep %s." % second
    time.sleep(second)
    print "Sleep %s seconds" % second

def test_print(second):
    print "print"

pool = eventlet.GreenPool()

for s in sleep_times:
    pool.spawn(will_sleep, s)

pool.waitall()
