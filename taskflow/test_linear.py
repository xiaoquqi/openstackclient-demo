#!/usr/bin/env python

import taskflow.engines
from taskflow.patterns import linear_flow as lf
from taskflow import task

class CallJim(task.Task):
    def execute(self, jim_number, *args, **kwargs):
        print("Calling Jim %s." % jim_number)

    def revert(self, jim_number, *args, **kwargs):
        print("Calling %s and apologizing." % jim_number)


class CallJoe(task.Task):
    def execute(self, joe_number, *args, **kwargs):
        print("Calling Joe %s." % joe_number)

    def revert(self, joe_number, *args, **kwargs):
        print("Calling %s and apologizing." % joe_number)


class CallRay(task.Task):
    def execute(self, ray_number, *args, **kwargs):
        raise IOError("Ray is not at home right now.")

    def revert(self, ray_number, *args, **kwargs):
        print("Calling %s and apologizing." % ray_number)

flow = lf.Flow("simple-linear").add(
    CallJim(),
    CallJoe(),
    CallRay()
)

try:
    taskflow.engines.run(flow,
            engine_conf={"engine": "serial"},
            store=dict(
                joe_number=444,
                jim_number=555,
                ray_number=666))
except Exception as e:
    print("Flow failed: %s" % e)
