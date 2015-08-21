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

from oslo.config import cfg
from oslo import messaging

from lib import utils

utils.log_init(True)

transport_url = 'rabbit://stackrabbit:sysadmin@127.0.0.1:5672/'
transport = messaging.get_transport(cfg.CONF, transport_url)
target = messaging.Target(topic='oslo_messaging.demo')
client = messaging.RPCClient(transport, target)
logging.info("Call remote test()")
ret = client.call(ctxt={}, method='test', arg='myarg')
logging.info("Remote test() return")

logging.info("Call remote stop()")
cctxt = client.prepare(namespace='control', version='2.0')
cctxt.cast({}, 'stop')
logging.info("Remote stop() return")
