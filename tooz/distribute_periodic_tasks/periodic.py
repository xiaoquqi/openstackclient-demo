#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_log import log as logging
import time

from oslo_config import cfg
from oslo_service import periodic_task
from oslo_service import threadgroup

import coordinator

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class Host(object):
    """This is a Demo class"""

    def __init__(self, hostname):
        self.id = hostname
        self.hostname = hostname

    def __str__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.hostname)

    def ping(self):
        time.sleep(5)
        return True


def _make_periodic_tasks():

    class PeriodicTasks(periodic_task.PeriodicTasks):
        hr = coordinator.HashRing("zookeeper://localhost:2181",
                                  "distribution_tasks")
        
        def __init__(self):
            super(PeriodicTasks, self).__init__(CONF)

        @periodic_task.periodic_task(spacing=5)
        def heartbeat(self, ctx):
            self.hr.heartbeat()

        @periodic_task.periodic_task(spacing=20)
        def ping_hosts(self, ctx):
            LOG.info("Starting periodic task...")
            hosts_to_ping = [Host("192.168.10.%d" % i) for i in range(20)]
            je_to_manage = self.hr.get_subset(hosts_to_ping)
            for host in je_to_manage:
                LOG.info("Pinging %s..." % host)
                host.ping()

    return PeriodicTasks()

def setup():
    tg = threadgroup.ThreadGroup()
    workers_number = 1

    for t in range(workers_number):
        pt = _make_periodic_tasks()
        tg.add_dynamic_timer(pt.run_periodic_tasks,
                             initial_delay=10,
                             periodic_interval_max=10,
                             context=None)
