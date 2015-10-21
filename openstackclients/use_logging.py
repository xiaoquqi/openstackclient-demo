#!/usr/bin/env python

import os
import sys

possible_topdir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, "lib", "__init__.py")):
        sys.path.insert(0, os.path.join(possible_topdir))
current_dir = os.path.normpath(os.path.join(
        os.path.abspath(sys.argv[0]), os.pardir))

import logging

from lib import utils

debug = False
utils.log_init(debug)

logging.debug("this is a debug message")
logging.info("this is a info message")
logging.warning("this is a warning message")
logging.error("this is a error message")
