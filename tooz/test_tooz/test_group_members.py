#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
import time
 
from tooz import coordination

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ZOOKEEPER_URL = "zookeeper://localhost:2181"
 
# Check that a client and group ids are passed as arguments
if len(sys.argv) != 3:
    print("Usage: %s <client id> <group id>" % sys.argv[0])
    sys.exit(1)
 
# Get the Coordinator object
c = coordination.get_coordinator(ZOOKEEPER_URL, sys.argv[1].encode())

# Start it (initiate connection).
c.start(start_heart=True)
 
group = sys.argv[2].encode()
 
# Create the group
try:
    c.create_group(group).get()
except coordination.GroupAlreadyExist:
    pass
 
# Join the group
c.join_group(group).get()
 
try:
    while True:
        # Print the members list
        #c.run_watchers()
        members = c.get_members(group).get()
        print("[%s]Current nodes in cluster: %s" % (
            current_time(), members))
        time.sleep(1)
except KeyboardInterrupt as e:
    print("CTRL C is pressed!")
finally:
    # Leave the group
    c.leave_group(group).get()
    print("[%s]After leave cluster nodes: %s" % (
        current_time(), c.get_members(group).get()))
    # Stop when we're done
    c.stop()
