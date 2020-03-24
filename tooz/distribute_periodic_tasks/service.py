#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_log import log as logging
import time

from oslo_config import cfg
from oslo_service import service

import periodic

LOG = logging.getLogger(__name__)

CONF = cfg.CONF


class Service(service.Service):

    @classmethod
    def create(cls):
        service_obj = cls()
        return service_obj

    def start(self):
        LOG.info("Service starting...")
        periodic.setup()

_launcher = None

def serve(server, workers=None):
    global _launcher
    if _launcher:
        raise RuntimeError(_('serve() can only be called once'))

    _launcher = service.launch(CONF, server, workers=workers,
                               restart_method='mutate')

def wait():
    _launcher.wait()
