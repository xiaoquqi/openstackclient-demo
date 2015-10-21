#!/usr/bin/env python

import glanceclient as glanceclient
from keystoneclient.auth.identity import v2
from keystoneclient import session
from neutronclient.neutron import client as neutronclient
import novaclient.client as novaclient

# keystone
auth_url = "http://192.168.56.102:5000/v2.0/"
username = "admin"
password = "sysadmin"
tenant_name = "demo"

# connects
auth = v2.Password(auth_url=auth_url,
                   username=username,
                   password=password,
                   tenant_name=tenant_name)
sess = session.Session(auth=auth)
token = sess.get_token()
print token
glance_endpoint = sess.get_endpoint(service_type="image", interface="public")
print glance_endpoint
neutron_endpoint = sess.get_endpoint(service_type="network", interface="public")

glance = glanceclient.Client(2, endpoint=glance_endpoint, token=token)
neutron = neutronclient.Client("2.0", endpoint_url=neutron_endpoint, token=token)
nova = novaclient.Client(2, session=sess)
