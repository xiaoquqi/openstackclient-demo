#!/usr/bin/env python

import json
import requests

AUTH_URL = "http://192.168.56.102:5000/v2.0"
USERNAME = "demo"
PASSWORD = "sysadmin"
TENANT_NAME = "demo"

auth_body = {
    "auth": {
        "tenantName": TENANT_NAME,
        "passwordCredentials": {
            "username": USERNAME,
            "password": PASSWORD
        }
    }
}

headers = {"Content-Type": "application/json"}

r = requests.post(AUTH_URL + "/tokens",
        data=json.dumps(auth_body),
        headers=headers)
resp = r.json()

token = resp["access"]["token"]["id"]
print "token is", token
