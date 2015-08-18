#!/usr/bin/env python

import eventlet
from eventlet.green import urllib2

eventlet.monkey_patch(os=False, thread=False)


urls = [
    "http://www.sina.com.cn",
    "http://baidu.com",
    "http://163.com",
]


def fetch(url):
    return urllib2.urlopen(url).read()


pool = eventlet.GreenPool()

for body in pool.imap(fetch, urls):
    print("got body", len(body))
