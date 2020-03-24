#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
import subprocess
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
 
# Join the partitioned group
p = c.join_partitioned_group(group)
 
class Host(object):
    def __init__(self, hostname):
        self.hostname = hostname
 
    def __tooz_hash__(self):
        """Returns a unique byte identifier so Tooz
           can distribute this object."""
        return self.hostname.encode()
 
    def __str__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.hostname)
 
    def ping(self):
        time.sleep(2)
        return True

hosts_to_ping = [Host("192.168.10.%d" % i) for i in range(20)]

print("[%s]Waiting 10 seconds for other members..." % current_time())
time.sleep(10)
print("[%s]Current members: %s" % (
    current_time(), c.get_members(group).get()))
 
try:
    while True:
        for host in hosts_to_ping:
            c.run_watchers()
            if p.belongs_to_self(host):
                print("[%s]%s belongs to %s" % (
                    current_time(), host, p.members_for_object(host)))
                if host.ping():
                    pass
        print("=" * 60)
        print("Waiting for next loop...")
        time.sleep(20)
except KeyboardInterrupt as e:
    print("CTRL C is pressed!")
finally:
    # Leave the group
    c.leave_group(group).get()
 
    # Stop when we're done
    c.stop()
