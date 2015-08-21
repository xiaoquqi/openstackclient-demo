#!/usr/bin/env python

import os
import sys

possible_topdir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, "lib", "__init__.py")):
        sys.path.insert(0, os.path.join(possible_topdir))
current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))

import logging

from lib import utils
from oslo_config import cfg
import oslo_messaging
import time

utils.log_init(True)

class ServerControlEndpoint(object):

    target = oslo_messaging.Target(namespace='control',
                                   version='2.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        logging.info("Server stop is called.")
        time.sleep(3)
        logging.info("Stop over")

class TestEndpoint(object):

    def test(self, ctx, arg):
        logging.info("Test is called, Sleeping 3 seconds")
        time.sleep(3)
        logging.info("Sleep over")
        return arg

transport_url = 'rabbit://stackrabbit:sysadmin@127.0.0.1:5672/'
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
target = oslo_messaging.Target(topic='oslo_messaging.demo', server='demo')
endpoints = [
    ServerControlEndpoint(None),
    TestEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
server.start()
server.wait()
