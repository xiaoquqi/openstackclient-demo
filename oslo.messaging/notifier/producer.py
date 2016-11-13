#!/usr/bin/env python
# coding: utf-8

import logging
import uuid

from oslo.config import cfg
from oslo import messaging

logging.basicConfig()
log = logging.getLogger()

log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

transport_url = 'rabbit://stackrabbit:sysadmin@127.0.0.1:5672/'
transport = messaging.get_transport(cfg.CONF, transport_url)

driver = 'messaging'

notifier = messaging.Notifier(transport, driver=driver, publisher_id='testing', topic='monitor')

notifier.info({'some': 'context'}, 'compute.create_instance', {'heavy': 'payload'})
notifier.error({'some': 'context'}, 'compute.create_instance', {'heavy': 'payload'})
notifier.warn({'some': 'context'}, 'compute.create_instance', {'heavy': 'payload'})
