#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_config import cfg
from oslo_log import log as logging

import service

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
DEBUG = True

logging.register_options(CONF)
logging.setup(CONF, DEBUG)


server = service.Service.create()
workers = 1

service.serve(server, workers=workers)
service.wait()
