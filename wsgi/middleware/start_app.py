from paste import httpserver
from paste.deploy import loadapp

import os
import sys

current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))
INI_PATH = os.path.join(current_dir, 'paste.ini')

wsgi_app = loadapp('config:' + INI_PATH)
httpserver.serve(wsgi_app, host='0.0.0.0', port=9090)
