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

import glanceclient as glanceclient
from keystoneclient.auth.identity import v2
from keystoneclient import session

from lib import utils
utils.log_init(False)

# keystone
auth_url = "http://192.168.56.102:5000/v2.0/"
username = "admin"
password = "sysadmin"
tenant_name = "demo"

# glance
image_name = "Ubuntu 12.04 64bit"
image_filename = "ubuntu_server_12.04_x64.qcow2"
image_path = os.path.join(current_dir, "images", image_filename)

# connects
auth = v2.Password(auth_url=auth_url,
                   username=username,
                   password=password,
                   tenant_name=tenant_name)
sess = session.Session(auth=auth)
token = sess.get_token()
glance_endpoint = sess.get_endpoint(service_type="image", interface="public")

glance = glanceclient.Client(2, endpoint=glance_endpoint, token=token)

def clean_image():
    images = glance.images.list()
    for i in images:
        if i.name == image_name:
            logging.info("Deleting image %s..." % i.name)
            glance.images.delete(i.id)

def upload_image_to_glance(sess):
    """Do all glance demo in this method"""
    new_image = glance.images.create(name=image_name,
                                     disk_format="qcow2",
                                     container_format="bare",
                                     min_disk=10,
                                     visibility="public")
    logging.info("Current image status: %s" % new_image.status)

    glance.images.upload(new_image.id, open(image_path, "rb"))
    time.sleep(5)
    new_image = glance.images.get(new_image.id)
    logging.info("Current image status: %s" % new_image.status)
    return new_image

upload_image_to_glance(sess)
clean_image()
