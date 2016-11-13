import oslo_messaging

topic_name = "oslo_messaging.ubuntu"
hostname = "ubuntu"

target = oslo_messaging.Target(topic=topic_name, server=hostname)
