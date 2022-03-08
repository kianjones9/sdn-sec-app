from __future__ import annotations
from random import choices
import requests
import argparse
import json

#ONOS Login Requirements
onos_username = 'onos'
onos_password = 'rocks'


#argparse to allow for usability with arguments & options
parser = argparse.ArgumentParser(
    description='Interact with ONOS controller via REST api')

parser.add_argument('--GET', type=str, choices=["devices", "flows"],
                    help='GET information')
parser.add_argument('--CREATE', type=str, choices=["flows"],
                    help='POST a new flow', default="flows")

args = vars(parser.parse_args())


#GET Devices
if args['GET'] == "devices":
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    r = response.json()
    
    print("DEVICES:")
    for dev in r["devices"]:
        print(f'ID: {dev["id"]}| ONLINE: {dev["available"]} | TYPE: {dev["type"]} | HW: {dev["hw"]}| VER: {dev["sw"]} | IP: {dev["annotations"]["managementAddress"]}')

#GET Flows
elif args['GET'] == "flows":
   onos_url = 'http://localhost:8181/onos/v1/flows'
   response = requests.get(onos_url, auth=(onos_username, onos_password))
   r = response.json()

   print("FLOWS:")
   for i in range(10):
        print(f'GID: {r["flows"][i]["groupId"]} | ID: {r["flows"][i]["id"]} | Device: {r["flows"][i]["deviceId"]} | PACKETS: {r["flows"][i]["packets"]} | {r["flows"][i]["treatment"]["instructions"]} | {r["flows"][i]["selector"]["criteria"]}')
   
 
#POST Flow
elif args['CREATE'] == "flows":
    onos_url = 'http://localhost:8181/onos/v1/flows/of%3A00003eb297d33847?appId=22'
    f = open("flow_lib.json")
    payload = f.read()

    response = requests.post(onos_url, auth=(
        onos_username, onos_password), data=payload)
    print(response.text)


else:
    print("invalid usage")

