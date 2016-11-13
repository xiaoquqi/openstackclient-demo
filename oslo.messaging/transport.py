import oslo_messaging
from oslo_config import cfg

transport_url = "rabbit://stackrabbit:sysadmin@127.0.0.1:5672/"
transport = oslo_messaging.get_transport(cfg.CONF, transport_url)
