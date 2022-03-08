import re
from flask import Flask, render_template
import datetime
import requests
import json
import time

#read in flow libs
ooga = open("./../flow_lib.json")
flow_lib = json.loads(ooga.read())
ooga.close()

#ONOS Login Requirements
onos_username = 'onos'
onos_password = 'rocks'

#List all devices
def deviceslist():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    devresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    r = devresponse.json()
    t=[]
    for dev in r["devices"]: 
        t.append(f'ID: {dev["id"]}| ONLINE: {dev["available"]} | TYPE: {dev["type"]} | HW: {dev["hw"]}| VER: {dev["sw"]} | IP: {dev["annotations"]["managementAddress"]}')
    return t


#List all Flows
def flowlist():
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        f.append(f'GID: {i["groupId"]} | ID: {i["id"]} | Device: {i["deviceId"]} | PACKETS: {i["packets"]} | {i["treatment"]["instructions"]} | {i["selector"]["criteria"]}')
    return f

#Count of flows
def flowcount():
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        f.append(f'GID: {i["groupId"]} | ID: {i["id"]} | Device: {i["deviceId"]} | PACKETS: {i["packets"]} | {i["treatment"]["instructions"]} | {i["selector"]["criteria"]}')
    return len(f)

#List of online Devices
def onlinedevices():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==True:
            q.append(f'ID: {dev["id"]}')
    return q

#List of offline Devices
def offlinedevices():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==False:
            q.append(f'ID: {dev["id"]}')
    return q

#Count of online Devices            
def onlinecount():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==True:
            q.append(f'ID: {dev["id"]}')
       
    return len(q)

#Count of offline Devices            
def offlinecount():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==False:
            q.append(f'ID: {dev["id"]}')
       
    return len(q)

#Packet Count
def packetcount():
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        f.append((f'{i["packets"]}'))
    
    intlist = [int(i) for i in f]

    Sum = sum(intlist)
    
    #print(Sum)
    return Sum

#Packets over time
def avgpackets():
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        f.append((f'{i["packets"]}'))
    intlist = [int(i) for i in f]
    Sum1 = sum(intlist)
    print("sum1")
    time.sleep(10)
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        f.append((f'{i["packets"]}'))
    intlist = [int(i) for i in f]
    Sum2 = sum(intlist)
    
    avg = (Sum2 - Sum1)/10
    return avg


app = Flask(__name__)


#Main Pages (Nav bar pages)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

#Devices
@app.route('/devices')
def devices():
    return render_template('devices.html', data=deviceslist(), online=onlinedevices(),count=onlinecount())

#Flows
@app.route('/flows')
def flows():
    return render_template('flows.html', data=flowlist())

#Statistics
@app.route('/stats')
def stats():
    return render_template('stats.html',onlinecount=onlinecount(),onlinedevices=onlinedevices(),flowcount=flowcount(), flows=flowlist(), packetcount=packetcount(),offlinecount=offlinecount(),offlinedevices=offlinedevices())

#Configure play
@app.route('/configure')
def configure():
    return render_template('configure.html')


#Apply Flow Actions
@app.route('/DemoDrop', methods = ['POST'])
def DemoDrop():
    payload = flow_lib["demo_drop"]
    onos_url = f'http://localhost:8181/onos/v1/flows/{payload["deviceId"]}?appId=1'

    response = requests.post(onos_url, auth=(
        onos_username, onos_password), json=payload)
    if (response.status_code) == "200":
        status = "OK"
    else:
        status = (response.status_code)
    return status

@app.route('/DemoAccept', methods=['POST'])
def DemoAccept():
    testitem = "Flow Applied"
    return render_template('configure.html', testitem=testitem)

@app.route('/pullstats', methods = ['GET'])
def pullstats():
    return render_template('stats.html',onlinecount=onlinecount(),onlinedevices=onlinedevices(),flowcount=flowcount(), flows=flowlist(), packetcount=packetcount(),offlinecount=offlinecount(),offlinedevices=offlinedevices(), avgpackets=avgpackets())
