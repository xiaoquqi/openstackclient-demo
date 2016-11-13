#!/usr/bin/env python

import sys
from oslo_config import cfg

OPTS = [
    cfg.StrOpt("host",
               default="demo.com",
               help="Name of the host."),
    cfg.IntOpt("workers",
               default=1,
               help="Number of workers for collector service.")
]
cfg.CONF.register_opts(OPTS)

CLI_OPTS = [
    cfg.StrOpt("os-tenant-id",
               deprecated_group="DEFAULT",
               default="default-os-tenant-id",
               help="Tenant ID to use for OpenStack service access."),
    cfg.BoolOpt("insecure",
                default=False,
                help="Disable X.509..."),
    cfg.ListOpt("list_multiple",
                default=[],
                help="list multiple test"),
    cfg.MultiStrOpt("multiple",
                default=[],
                help="multiple test"),
]
cfg.CONF.register_opts(CLI_OPTS, group="service_credentials")

CONF = cfg.CONF

print "[default]host is", CONF.host
print "[default]os-tenant-id is", CONF.service_credentials.os_tenant_id

CONF(sys.argv[1:], project="demo")

print "[new]host is", CONF.host
print "[new]os-tenant-id is", CONF.service_credentials.os_tenant_id
print "[new]list multiple is", CONF.service_credentials.list_multiple
print "[new]multiple is", CONF.service_credentials.multiple
