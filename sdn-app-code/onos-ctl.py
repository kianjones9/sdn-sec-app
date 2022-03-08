from __future__ import annotations
import requests
import argparse
import json

#ONOS Login Requirements
onos_username = 'onos'
onos_password = 'rocks'

def auto_int(x):
    return int(x, base=16)

#argparse to allow for usability with arguments & options
parser = argparse.ArgumentParser(
    description='Interact with ONOS controller via REST api')

parser.add_argument('--GET', type=str, choices=["devices", "flows"],
                    help='GET information')

f = open("flow_lib.json")
flow_lib = json.loads(f.read())
f.close()

parser.add_argument('--CREATE', type=str, choices=flow_lib.keys(),
                    help='POST a flow')

parser.add_argument('--DELETE', type=auto_int, help='DELETE a flow')

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
elif args['CREATE']:

    payload = flow_lib[args["CREATE"]]
    onos_url = f'http://localhost:8181/onos/v1/flows/{payload["deviceId"]}?appId=1'

    response = requests.post(onos_url, auth=(
        onos_username, onos_password), json=payload)
    print(response.status_code)


elif args['DELETE']:
    
    flow_id = args["DELETE"]
    print("Enter Device ID: ")
    dev_id = input() or "of:00003c2c301b9c81"

    url = f"http://localhost:8181/onos/v1/flows/{dev_id}/{flow_id}"

    r = requests.delete(url, auth=(onos_username, onos_password))

    print(url)
    print(r.status_code)

else:
    print("invalid usage")

