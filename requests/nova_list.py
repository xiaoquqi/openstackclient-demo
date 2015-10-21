#!/usr/bin/env python

import json
import requests
import sys

if len(sys.argv) < 2:
    print "No token or endpoints given"
    sys.exit()

token = sys.argv[1]
endpoint = sys.argv[2]

url = endpoint + "/servers/detail"

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": token
}

r = requests.get(url, headers=headers)
print r.status_code
print r.text
