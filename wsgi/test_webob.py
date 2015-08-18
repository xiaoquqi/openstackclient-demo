#!/usr/bin/env python

"""Hello World using WebOb, Paste + WSGI """
from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp

import os
import sys

current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))
INI_PATH = os.path.join(current_dir, 'wsgi_webob.ini')

@wsgify
def application(request):
    return Response('Hello, World of WebOb!')

def app_factory(global_config, **local_config):
    return application

wsgi_app = loadapp('config:' + INI_PATH)

httpserver.serve(wsgi_app, host='0.0.0.0', port=9090)
