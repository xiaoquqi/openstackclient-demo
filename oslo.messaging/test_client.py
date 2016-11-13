#!/usr/bin/env python

import oslo_messaging

from transport import transport

target = oslo_messaging.Target(topic="oslo_messaging.ubuntu")
client = oslo_messaging.RPCClient(transport, target)
ret = client.prepare(namespace="control", version="2.0")

print "Call will wait for feedback"
call_ret = ret.call(ctxt={}, method="sleep", arg="call_arg")
print "Call return value %s" % call_ret
print "Call feedback"

print "-" * 30

print "Cast will not wait for feedback"
cast_ret = ret.cast(ctxt={}, method="sleep", arg="cast_arg")
print "Cast feedback"
