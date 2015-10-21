#!/usr/bin/env python

import logging
import os
import sys
import time

possible_topdir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, "lib", "__init__.py")):
        sys.path.insert(0, os.path.join(possible_topdir))
current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))

from keystoneclient.auth.identity import v2
from keystoneclient import session
from neutronclient.neutron import client as neutronclient

from lib import utils
utils.log_init(True)

# keystone
auth_url = "http://192.168.56.102:5000/v2.0/"
username = "admin"
password = "sysadmin"
tenant_name = "demo"

# network
public_network_name = "public"

app_network = "app_network"
app_network_cidr = "20.0.0.0/24"

db_network = "db_network"
db_network_cidr = "30.0.0.0/24"

router_name = "app-db-router"

# connects
auth = v2.Password(auth_url=auth_url,
                   username=username,
                   password=password,
                   tenant_name=tenant_name)
sess = session.Session(auth=auth)
token = sess.get_token()
neutron_endpoint = sess.get_endpoint(service_type="network", interface="public")

neutron = neutronclient.Client("2.0", endpoint_url=neutron_endpoint, token=token)

def create_network(name, cidr):
    """Create network and subnet"""
    subnet_name = "%s_subnet" % name
    net = neutron.create_network({
        "network": {
            "name": name,
            "admin_state_up": True
        }
    })
    subnet = neutron.create_subnet({
        "subnet": {
            "name": subnet_name,
            "network_id": net["network"]["id"],
            "ip_version": 4,
            "cidr": cidr,
            "enable_dhcp": True,
            "dns_nameservers": ["8.8.8.8"]
        }
    })
    return net, subnet

def create_router(app_net, db_net):
    # create router
    app_subnet_id = app_net["subnet"]["id"]
    db_subnet_id = db_net["subnet"]["id"]
    router = neutron.create_router({
        "router": {
            "name": router_name,
            "admin_state_up": True
        }
    })
    router_id = router["router"]["id"]
    # add router gateway
    public_network = None
    networks = neutron.list_networks()["networks"]
    for net in networks:
        if net["name"] == public_network_name:
            public_network = net
            break
    # add gateway
    neutron.add_gateway_router(router_id, {
        "network_id": net["id"]
    })
    # add router interface
    neutron.add_interface_router(router_id, {
        "subnet_id": app_subnet_id
    })
    neutron.add_interface_router(router_id, {
        "subnet_id": db_subnet_id
    })

app_net, app_subnet = create_network(app_network, app_network_cidr)
db_net, db_subnet = create_network(db_network, db_network_cidr)
create_router(app_subnet, db_subnet)
