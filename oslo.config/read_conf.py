#!/usr/bin/env python

# Script to read OpenStack config file
# python read_conf.py --config-file /etc/nova/nova.conf

import sys

from oslo_config import cfg

CONF = cfg.CONF
CONF(sys.argv[1:])

print CONF.list_all_sections()
