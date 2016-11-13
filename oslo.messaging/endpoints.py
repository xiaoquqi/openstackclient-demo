import oslo_messaging
import time

class DemoEndpoint(object):

    target = oslo_messaging.Target(namespace="control", version="2.0")

    def sleep(self, ctx, arg):
        print arg
        sleep_time = 3
        print "I will sleep for %s seconds" % sleep_time
        time.sleep(sleep_time)
        print "Sleep %s is over" % sleep_time
        return "sleep return"
