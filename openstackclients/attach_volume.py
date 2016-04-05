#!/usr/bin/env python

from cinderclient import client
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
nova = novaclient.Client(2, session=sess)

cinder = client.Client('1', username, password, tenant_name, auth_url)
print cinder.volumes.list()

myvol = cinder.volumes.create(display_name="test-vol", size=1)
nova.volumes.create_server_volume("4be7d4a4-2a8f-4ea3-b5fb-3eb28504cfdc", myvol.id, "/dev/sdb")















