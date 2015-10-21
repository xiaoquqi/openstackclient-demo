#!/usr/bin/env python

import json
import requests
import sys
import time

if len(sys.argv) < 2:
    print "No token or endpoints given"
    sys.exit()

IMAGE_ID = "027f4e0b-d37b-4aaa-9642-7e858d203a1b"
FLAVOR_ID = "1"
NETWORK_ID = "b913aea5-e9e5-4b6b-a87a-3633a273f127"

token = sys.argv[1]
endpoint = sys.argv[2]

url = endpoint + "/servers"

headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": token
}

server_body = {
    "server": {
        "name": "server-test-1",
        "imageRef": IMAGE_ID,
        "flavorRef": FLAVOR_ID,
        "max_count": 1,
        "min_count": 1,
        "networks": [
            {
                "uuid": NETWORK_ID
            }
        ],
        "security_groups": [
            {
                "name": "default"
            }
        ]
    }
}

r = requests.post(url, headers=headers, data=json.dumps(server_body))
print r.status_code
print r.text
instance_id = r.json()["server"]["id"]
print instance_id

def is_instance_ready(instance_id):
    instance_url = endpoint + "/servers/" + instance_id
    req = requests.get(instance_url, headers=headers)
    print req.json()
    status = req.json()["server"]["status"]
    return status == "ACTIVE"

while not is_instance_ready(instance_id):
    time.sleep(5)
    print "Instance is still starting..."
