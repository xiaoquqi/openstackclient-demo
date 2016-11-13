#!/usr/bin/env python

import oslo_messaging

from endpoints import DemoEndpoint
from target import target
from transport import transport

endpoints = [
    DemoEndpoint()
]

server = oslo_messaging.get_rpc_server(transport, target, endpoints,
        executor="blocking")

print "Starting RPC server..."

server.start()
server.wait()
