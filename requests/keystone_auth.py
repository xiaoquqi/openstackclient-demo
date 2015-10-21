#!/usr/bin/python

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

r = requests.get(AUTH_URL)
print r.status_code
print r.headers

r = requests.post(
        AUTH_URL + "/tokens",
        data=json.dumps(auth_body),
        headers=headers)
resp = r.json()
print "resp is", resp
print "-" * 20

token = resp["access"]["token"]["id"]
print "token is", token

endpoints = resp["access"]["serviceCatalog"]
for e in endpoints:
    print e
    print "-" * 20
