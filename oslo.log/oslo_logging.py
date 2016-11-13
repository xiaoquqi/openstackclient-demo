#!/usr/bin/env python

from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

# Oslo Logging uses INFO as default
LOG.info("Oslo Logging")
LOG.warning("Oslo Logging")
LOG.error("Oslo Logging")
