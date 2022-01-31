from random import choices
import requests
import argparse


onos_username = 'onos'
onos_password = 'rocks'


parser = argparse.ArgumentParser(description='Interact with ONOS controller via REST api')


parser.add_argument('--GET', type=str, choices=["devices", "flows"],
                    help='GET information')
parser.add_argument('--POST', type=str,choices=["flows"],
                    help='Create a new flow', default="flows")



args = vars(parser.parse_args())

if args['GET'] == "devices":
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    print(response.json())
elif args['GET'] == "flows":
   onos_url = 'http://localhost:8181/onos/v1/flows'
   response = requests.get(onos_url, auth=(onos_username, onos_password))
   print(response.json())

   
else:
    print("invalid usage")



"""
#OpenDayLight RESTCONF API settings.
onos_url = 'http://localhost:8181/onos/v1/devices'
onos_username = 'onos'
onos_password = 'rocks'

# Fetch information from API.
response = requests.get(onos_url, auth=(onos_username, onos_password))


print(response.json())

"""















"""
# Find information about nodes in retrieved JSON file.
for nodes in response.json()['network-topology']['topology']:

    # Walk through all node information.
    node_info = nodes['node']

    # Look for MAC and IP addresses in node information.
    for node in node_info:
        try:
            ip_address = node['host-tracker-service:addresses'][0]['ip']
            mac_address = node['host-tracker-service:addresses'][0]['mac']
            print('Found host with MAC address %s and IP address %s' % (mac_address, ip_address))
        except:
            pass
"""