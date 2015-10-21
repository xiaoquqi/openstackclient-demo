#!/usr/bin/env python

"""This demo is used to show how to use OpenStack internal client to create
VMs with networks.

Tested on OpenStack Kilo.

Author: Ray(xiaoquqi@gmail.com)
"""


import os
import sys

possible_topdir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, "lib", "__init__.py")):
        sys.path.insert(0, os.path.join(possible_topdir))
current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))

import logging
import optparse
import time

import glanceclient as glanceclient
from keystoneclient.auth.identity import v2
from keystoneclient import session
from neutronclient.neutron import client as neutronclient
import novaclient.client as novaclient

from lib import utils

# keystone
auth_url = "http://192.168.56.102:5000/v2.0/"
username = "admin"
password = "sysadmin"
tenant_name = "demo"

# glance
image_name = "Ubuntu 12.04 64bit"
image_filename = "ubuntu_server_12.04_x64.qcow2"
image_path = os.path.join(current_dir, "images", image_filename)

# network
public_network_name = "public"

app_network = "app_network"
app_network_cidr = "20.0.0.0/24"

db_network = "db_network"
db_network_cidr = "30.0.0.0/24"

router_name = "app-db-router"

# instance
flavor_name = "m1.small"

app_vm_name = "wordpress"
db_vm_name = "mysql"

sec_group_name = "demo-sec"

keypair_name = "ray-keypair"
keypair_pub_path = "/home/sysadmin/.ssh/id_rsa.pub"
keypair_pub = open(keypair_pub_path, "rb").read()

db_name = "wordpress"
db_username = "wordpressuser"
db_password = "wordpress-secret"

app_script = '''#!/usr/bin/env bash
cat << EOF | tee /etc/apt/sources.list
deb http://200.21.0.30/ubuntu/ precise main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-security main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-updates main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-proposed main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-backports main restricted universe multiverse
EOF
sudo apt-get update
sudo apt-get install -y unzip
sudo apt-get install -y apache2 php5-gd libapache2-mod-php5 php5-mysql php5
sudo apt-get install -y mysql-client-core-5.5
wget http://200.21.1.61:10000/wordpress-4.2.4.zip -O /tmp/wordpress.zip
unzip /tmp/wordpress.zip -d /var/www
cp /var/www/wordpress/wp-config-sample.php /var/www/wordpress/wp-config.php
sed -i s/"define('DB_NAME', 'database_name_here');"/"define('DB_NAME', '%s');"/ /var/www/wordpress/wp-config.php
sed -i s/"define('DB_USER', 'username_here');"/"define('DB_USER', '%s');"/ /var/www/wordpress/wp-config.php
sed -i s/"define('DB_PASSWORD', 'password_here');"/"define('DB_PASSWORD', '%s');"/ /var/www/wordpress/wp-config.php
sed -i s/"define('DB_HOST', 'localhost');"/"define('DB_HOST', '%s');"/ /var/www/wordpress/wp-config.php
'''

db_script = '''#!/usr/bin/env bash
cat << EOF | tee /etc/apt/sources.list
deb http://200.21.0.30/ubuntu/ precise main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-security main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-updates main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-proposed main restricted universe multiverse
deb http://200.21.0.30/ubuntu/ precise-backports main restricted universe multiverse
EOF
sudo apt-get update
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password sysadmin'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password sysadmin'
sudo apt-get install -y mysql-server
sudo sed -i s/'127.0.0.1'/'0.0.0.0'/ /etc/mysql/my.cnf
sudo service mysql restart
mysql -uroot -psysadmin << EOF
CREATE DATABASE IF NOT EXISTS {} default charset utf8 COLLATE utf8_general_ci;
GRANT ALL ON {}.* TO {}@'%' IDENTIFIED BY '{}';
FLUSH PRIVILEGES;
exit;
EOF
'''.format(db_name, db_name, db_username, db_password)

# connects
auth = v2.Password(auth_url=auth_url,
                   username=username,
                   password=password,
                   tenant_name=tenant_name)
sess = session.Session(auth=auth)
token = sess.get_token()
glance_endpoint = sess.get_endpoint(service_type="image", interface="public")
neutron_endpoint = sess.get_endpoint(service_type="network", interface="public")

glance = glanceclient.Client(2, endpoint=glance_endpoint, token=token)
neutron = neutronclient.Client("2.0", endpoint_url=neutron_endpoint, token=token)
nova = novaclient.Client(2, session=sess)

def clean_all():
    """Remove all created resources

    Including VMs, Networks and Images
    """
    instances = nova.servers.list()
    for n in instances:
        if n.name in (app_vm_name, db_vm_name):
            logging.info("Deleting instance %s..." % n.name)
            nova.servers.delete(n.id)

    time.sleep(5)

    images = glance.images.list()
    for i in images:
        if i.name == image_name:
            logging.info("Deleting image %s..." % i.name)
            glance.images.delete(i.id)

    routers = neutron.list_routers()["routers"]
    for router in routers:
        if router["name"] == router_name:
            logging.info("Clear gateway on router %s" % router["name"])
            neutron.remove_gateway_router(router["id"])
            router_ports = neutron.list_ports(
                    device_id=router["id"])["ports"]
            for p in router_ports:
                subnet_id = p["fixed_ips"][0]["subnet_id"]
                logging.info("Removing port %s from router %s" % (
                    subnet_id, router["name"]))
                neutron.remove_interface_router(router["id"], {
                    "subnet_id": subnet_id
                })
            neutron.delete_router(router["id"])

    networks = neutron.list_networks()["networks"]
    for net in networks:
        if net["name"] in (app_network, db_network):
            logging.info("Deleting network %s" % net["name"])
            neutron.delete_network(net["id"])

    floating_ips = nova.floating_ips.list()
    for f_ip in floating_ips:
        if f_ip.instance_id is None:
            logging.info("Removing floating ip %s" % f_ip.ip)
            f_ip.delete()

    security_groups = neutron.list_security_groups()["security_groups"]
    for sec in security_groups:
        if sec["name"] == sec_group_name:
            logging.info("Removeing security group %s" % sec["name"])
            neutron.delete_security_group(sec["id"])

    keypairs = nova.keypairs.list()
    for key in keypairs:
        if key.name == keypair_name:
            logging.info("Removing keypairs %s" % key.name)
            key.delete()

def print_info(message):
    logging.info("------------------------------------------")
    logging.info(message)
    logging.info("------------------------------------------")

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

def get_flavor_id():
    print_info("Retreiving all flavors...")
    flavors = nova.flavors.list()
    flavor_id = None
    for f in flavors:
        if f.name == flavor_name:
            flavor_id = f.id
            logging.info("Flavor %s id is %s" %(flavor_name, flavor_id))
            return flavor_id

    if flavor_id is None:
        logging.error("Can not find flavor %s" % flavor_name)
        sys.exit(1)

def create_instance_in_nova(sess, image):
    """Do all nova demo in this method"""
    flavor_id = get_flavor_id()

    create_sec_group()
    import_keypair()

    app_net, app_subnet = create_network(app_network, app_network_cidr)
    db_net, db_subnet = create_network(db_network, db_network_cidr)
    create_router(app_subnet, db_subnet)

    app_net_id = app_net["network"]["id"]
    db_net_id = db_net["network"]["id"]
    db_instance = nova.servers.create(
            db_vm_name, image.id,
            flavor_id, nics=[{"net-id": db_net_id}],
            key_name=keypair_name,
            security_groups=[sec_group_name],
            userdata=db_script)
    time.sleep(10)
    db_fixed_ip = nova.servers.get(db_instance.id).networks["db_network"][0]
    logging.info("Database fixed ip is %s" % db_fixed_ip)
    app_userdata = app_script % (db_name, db_username, db_password, db_fixed_ip)
    app_instance = nova.servers.create(
            app_vm_name, image.id,
            flavor_id, nics=[{"net-id": app_net_id}],
            key_name=keypair_name,
            security_groups=[sec_group_name],
            userdata=app_userdata)
    time.sleep(20)
    floating_ip = nova.floating_ips.create()
    nova.servers.add_floating_ip(db_instance.id, floating_ip.ip)
    logging.info("Access %s via %s" %(db_instance.name, floating_ip.ip))

    floating_ip = nova.floating_ips.create()
    nova.servers.add_floating_ip(app_instance.id, floating_ip.ip)
    logging.info("Access %s via %s" %(app_instance.name, floating_ip.ip))

    servers = nova.servers.list(search_opts={"all_tenants": True})
    print_info("Listing all instances...")
    for s in servers:
        logging.info(s.name)

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

def create_sec_group():
    sec_group = neutron.create_security_group({
        "security_group": {
            "name": sec_group_name
        }
    })
    neutron.create_security_group_rule({
        "security_group_rule": {
            "direction": "ingress",
            "port_range_min": 1,
            "port_range_max": 65535,
            "protocol": "tcp",
            "ethertype": "IPv4",
            "security_group_id": sec_group["security_group"]["id"]
        }
    })
    neutron.create_security_group_rule({
        "security_group_rule": {
            "direction": "egress",
            "port_range_min": 1,
            "port_range_max": 65535,
            "protocol": "tcp",
            "ethertype": "IPv4",
            "security_group_id": sec_group["security_group"]["id"]
        }
    })
    neutron.create_security_group_rule({
        "security_group_rule": {
            "direction": "ingress",
            "protocol": "icmp",
            "ethertype": "IPv4",
            "security_group_id": sec_group["security_group"]["id"]
        }
    })
    neutron.create_security_group_rule({
        "security_group_rule": {
            "direction": "egress",
            "protocol": "icmp",
            "ethertype": "IPv4",
            "security_group_id": sec_group["security_group"]["id"]
        }
    })

def import_keypair():
    nova.keypairs.create(keypair_name, public_key=keypair_pub)

def parse_args(argv):
    """Parses commaond-line arguments"""
    parser = optparse.OptionParser()
    parser.add_option("-d", "--debug", action="store_true",
            dest="debug", default=False,
            help="Enable debug message")
    return parser.parse_args(argv[1:])[0]

def main(argv):
    os.environ["LANG"] = "en_US.UTF8"
    options = parse_args(argv)
    utils.log_init(options.debug)

    clean_all()
    image = upload_image_to_glance(sess)
    create_instance_in_nova(sess, image)

if __name__ == "__main__":
    main(sys.argv)
