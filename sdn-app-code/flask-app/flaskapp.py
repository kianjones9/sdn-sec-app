from crypt import methods
from itertools import dropwhile
import re
from attr import NOTHING
from flask import Flask, jsonify, redirect, render_template
import datetime
import requests
import json
import time
from flask import request


#Read in flow libs
fileread = open("./../flow_lib.json")
flow_lib = json.loads(fileread.read())
fileread.close()

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
            q.append(f'ID: {dev["id"]}| ONLINE: {dev["available"]} | TYPE: {dev["type"]} | HW: {dev["hw"]}| VER: {dev["sw"]} | IP: {dev["annotations"]["managementAddress"]}')
    return q

#List of online Devices (shortened)
def onlinedevicesshort():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==True:
            q.append(f'ID: {dev["id"]}| ONLINE: {dev["available"]} | IP: {dev["annotations"]["managementAddress"]}')
    return q

#List of online Dev IDs
def onlinedeviceID():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==True:
            q.append(dev["id"])
    return q

#List of offline Devices
def offlinedevices():
    onos_url = 'http://localhost:8181/onos/v1/devices'
    response = requests.get(onos_url, auth=(onos_username, onos_password))
    p = response.json()
    q=[]
    for dev in p["devices"]:
        if dev["available"] ==False:
             q.append(f'ID: {dev["id"]}| ONLINE: {dev["available"]} | TYPE: {dev["type"]} | HW: {dev["hw"]}| VER: {dev["sw"]} | IP: {dev["annotations"]["managementAddress"]}')
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

#Get Flows with packets
def flowpackets():
    onos_url = 'http://localhost:8181/onos/v1/flows'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]
    for i in q["flows"]:
        if i["packets"] != 0:
            f.append(f'FLOW ID: {i["id"]} | PACKETS: {i["packets"]}')     
    return f


app = Flask(__name__)

#Home Page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


#Statistics Page
@app.route('/stats')
def stats():
    return render_template('stats.html',flowpackets=flowpackets(),devicedata=deviceslist(),onlinecount=onlinecount(),onlinedevices=onlinedevices(),flowcount=flowcount(), flows=flowlist(), packetcount=packetcount(),offlinecount=offlinecount(),offlinedevices=offlinedevices())

#Configure Page
@app.route('/configure')
def configure():
    return render_template('configure.html', devicedata=onlinedevicesshort(), onlinedeviceID=onlinedeviceID(),flowlibrary=flow_lib)


#Apply Library Flow Actions
@app.route('/libraryflow', methods = ['POST'])
def DemoDrop():
    payload = flow_lib["demo_drop"]
    
    data = json.dumps(request.form)
    f = json.loads(data)
    payload = (f['flowlib'])
    flowdev = (f['flowdev'])
    onos_url = f'http://localhost:8181/onos/v1/flows/{flowdev}?appId=1'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=payload)
   
    print(response.status_code)
    return (response.status_code)

@app.route('/DemoAccept', methods=['POST'])
def DemoAccept():
    testitem = "Flow Applied"
    return redirect('/configure')

@app.route('/pullstats', methods = ['GET'])
def pullstats():
    return render_template('stats.html',onlinecount=onlinecount(),onlinedevices=onlinedevices(),flowcount=flowcount(), flows=flowlist(), packetcount=packetcount(),offlinecount=offlinecount(),offlinedevices=offlinedevices(), avgpackets=avgpackets())

# Work in progress ############################################################################################################

#Custom Flow Post
@app.route('/customflow', methods = ['POST'])
def customflow():
    data = json.dumps(request.form)
    f = json.loads(data)
#general
    device = (f['device'])
    group = (f['group'])
    priority = (f['priority'])
#instruction
    # this is stupid, should be done in HTML but was messing with my script (relook at this)
    # itype = (f['instructiontype'])
    # if itype=="SEN1":
    #     itype = "OUTPUT"
    # if itype=="SEN2":
    #     itype = "L2MODIFICATION"
    # if itype=="SEN3":
    #     itype = "L3MODIFICATION"
    itype = (f['instructiontype'])  
    subtybe = (f['instructionsubtype'])
    iport = (f['instructionport'])
    imac = (f['instructionmac'])
    iipv4 = (f['instructionipv4'])
    #ivlan = (f['instructionvlan'])
#selector
    stype = (f['rad2'])
    if stype=="SEN4":
        stype = "ETH_TYPE"
    if stype=="SEN5":
        stype = "ETH_DST"
    if stype=="SEN6":
        stype = "ETH_SRC"
    if stype=="SEN7":
        stype = "IN_PORT"
    if stype=="SEN8":
        stype = "VLAN_VID"
    if stype=="SEN9":
        stype = "IPV4_DST"
    if stype=="SEN10":
        stype = "IPV4_SRC"

    ethtype = (f['selectorethtype'])
    sport = (f['selectorport'])
    smac = (f['selectormac'])
    sipv4 = (f['selectoripv4'])
    svlan = (f['selectorvlan'])

    print(device,group,priority,itype, subtybe, iport, imac, iipv4, stype, ethtype,sport,smac,sipv4,svlan)

#Treatment inserts (this is test stuff, might need to rethink this. OR could change form input to be radio button types and according fields)
  #  if(itype == "OUTPUT"):
   #     treatment = '"treatment":{"instructions":[{"type":"'+ itype + '","port":"'+ iport + '"}]}'
    
    #custom = '{"priority":'+ priority + ',"timeout":0,"isPermanent":true,"deviceId":"'+ device + '","treatment":{"instructions":[{"type":"'+ itype + '","port":"'+ iport + '"}]},"selector":{"criteria":[{"type":"ETH_TYPE","ethType":"0x88cc"}]}}'

    #customflowj = json.loads(custom)
    #print(customflowj)

    return redirect('/configure')

############################################################################################################

#Delete Flows
@app.route('/deleteflow', methods = ['POST'])
def deleteflow():
    data = (request.form)
    dev_id = (data["deletedev"])
    flow_id = (data["deleteflow"])
    flow_id = int(flow_id, base=16)
    print(flow_id)    
    url = f"http://localhost:8181/onos/v1/flows/{dev_id}/{flow_id}"
    r = requests.delete(url, auth=(onos_username, onos_password))
    print(url)
    print(r.status_code)
    return redirect('/configure')


# POLICY - Source IP Monitor PACKET LIMIT
@app.route('/srcmonitorpacket', methods = ['POST','GET'])
def srcmonitorpacket():

    #customID = 120 #SHOULD make this user definable

    data = json.dumps(request.form)
    f = json.loads(data)
    srcipv4 = (f['srcipv4'])
    ratelimit = int((f['ratelimit']))
    customID = int((f['customID']))
    deviceID = (f['device']) 
    print (srcipv4, ratelimit)

    payload = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"'+deviceID+'","treatment":{"instructions":[{"type":"OUTPUT","port":"CONTROLLER"}]},"selector":{"criteria":[{"type": "ETH_TYPE","ethType": "0x800"},{"type":"IPV4_SRC","ip":"'+srcipv4+'"}]}}'
    jsonpayload = json.dumps(payload)
    jsonpayload = json.loads(payload)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=jsonpayload)
 
    status = (response.status_code) 
    print(status)

    flowid = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/application/{customID}'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]

    for i in q["flows"]:
        if i["deviceId"] == deviceID:
            flowid = i["id"]
            break

    avg = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/{deviceID}/{flowid}'
    while avg < ratelimit:
        time.sleep(10)
        
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["packets"]}'))
        print(f)
       
        Sum1 = sum(f)
        time.sleep(10)
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["packets"]}'))
        Sum2 = sum(f)
        
        avg = (Sum2 - Sum1)/10
        print(avg) 

    print(q["flows"][0]["treatment"]["instructions"][0])

    q["flows"][0]["treatment"]["instructions"][0] = {"type": "OUTPUT", "port": "DROP"}
    print(q["flows"][0])
    foo = (q["flows"][0])
    [foo.pop(x) for x in ["groupId","state","liveType","life","lastSeen","bytes","id", "appId","packets","tableId","tableName"]]
    
    var = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"of:00003c2c301b9c81","treatment":{},"selector":{"criteria":[{"type":"ETH_TYPE","ethType":"0x800"},{"type":"IPV4_SRC","ip":"'+srcipv4+'"}]}}'
    data = json.dumps(var)
    data = json.loads(var)

    print(var)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=data)
    print(response)
    
    # Only thing left to maybe add would be threads OR when to restore rules after traffic is ok?



# POLICY - Destination IP Monitor PACKET LIMIT (WORK IN PROGRESS)
@app.route('/destmonitorpacket', methods = ['POST','GET'])
def destmonitorpacket():


    data = json.dumps(request.form)
    f = json.loads(data)
    destipv4 = (f['destipv4'])
    ratelimit = int((f['ratelimit']))
    customID = int((f['customID']))
    deviceID = (f['device']) 
    print (destipv4, ratelimit)

    payload = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"'+deviceID+'","treatment":{"instructions":[{"type":"OUTPUT","port":"CONTROLLER"}]},"selector":{"criteria":[{"type": "ETH_TYPE","ethType": "0x800"},{"type":"IPV4_SRC","ip":"'+destipv4+'"}]}}'
    jsonpayload = json.dumps(payload)
    jsonpayload = json.loads(payload)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=jsonpayload)
 
    status = (response.status_code) 
    print(status)

    flowid = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/application/{customID}'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]

    for i in q["flows"]:
        if i["deviceId"] == deviceID:
            flowid = i["id"]
            break


    avg = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/{deviceID}/{flowid}'
    while avg < ratelimit:
        time.sleep(10)
        
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["packets"]}'))
        print(f)
       
        Sum1 = sum(f)
        time.sleep(10)
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["packets"]}'))
        Sum2 = sum(f)
        
        avg = (Sum2 - Sum1)/10
        print(avg) 

    print(q["flows"][0]["treatment"]["instructions"][0])

    q["flows"][0]["treatment"]["instructions"][0] = {"type": "OUTPUT", "port": "DROP"}
    print(q["flows"][0])
    foo = (q["flows"][0])
    [foo.pop(x) for x in ["groupId","state","liveType","life","lastSeen","bytes","id", "appId","packets","tableId","tableName"]]
    
    var = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"of:00003c2c301b9c81","treatment":{},"selector":{"criteria":[{"type":"ETH_TYPE","ethType":"0x800"},{"type":"IPV4_SRC","ip":"'+destipv4+'"}]}}'
    data = json.dumps(var)
    data = json.loads(var)

    print(var)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=data)
    print(response)

    return redirect('/configure')

# POLICY - Source IP Monitor BYTE LIMIT (WIP)
@app.route('/srcmonitorbytes', methods = ['POST','GET'])
def srcmonitorbytes():


    data = json.dumps(request.form)
    f = json.loads(data)
    srcipv4 = (f['srcipv4'])
    ratelimit = int((f['ratelimit']))
    customID = int((f['customID']))
    deviceID = (f['device']) 
    print (srcipv4, ratelimit)


    payload = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"'+deviceID+'","treatment":{"instructions":[{"type":"OUTPUT","port":"CONTROLLER"}]},"selector":{"criteria":[{"type": "ETH_TYPE","ethType": "0x800"},{"type":"IPV4_SRC","ip":"'+srcipv4+'"}]}}'
    jsonpayload = json.dumps(payload)
    jsonpayload = json.loads(payload)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=jsonpayload)
 
    status = (response.status_code) 
    print(status)

    flowid = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/application/{customID}'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]

    for i in q["flows"]:
        if i["deviceId"] == deviceID:
            flowid = i["id"]
            break

    avg = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/{deviceID}/{flowid}'
    while avg < ratelimit:
        time.sleep(10)
        
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["bytes"]}'))
        print(f)
       
        Sum1 = sum(f)
        time.sleep(10)
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["bytes"]}'))
        Sum2 = sum(f)
        
        avg = (Sum2 - Sum1)/10
        print(avg) 

    print(q["flows"][0]["treatment"]["instructions"][0])

    q["flows"][0]["treatment"]["instructions"][0] = {"type": "OUTPUT", "port": "DROP"}
    print(q["flows"][0])
    foo = (q["flows"][0])
    [foo.pop(x) for x in ["groupId","state","liveType","life","lastSeen","bytes","id", "appId","packets","tableId","tableName"]]
    
    var = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"of:00003c2c301b9c81","treatment":{},"selector":{"criteria":[{"type":"ETH_TYPE","ethType":"0x800"},{"type":"IPV4_SRC","ip":"'+srcipv4+'"}]}}'
    data = json.dumps(var)
    data = json.loads(var)

    print(var)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=data)
    print(response)
    
    # Only thing left to maybe add would be threads OR when to restore rules after traffic is ok?


    # POLICY - Destination IP Monitor BYTE LIMIT (WIP)
@app.route('/destmonitorbytes', methods = ['POST','GET'])
def destmonitorbytes():

    customID = 120 #Should make this user definable

    data = json.dumps(request.form)
    f = json.loads(data)
    destipv4 = (f['destipv4'])
    ratelimit = int((f['ratelimit']))
    customID = int((f['customID']))
    deviceID = (f['device']) 
    print (destipv4, ratelimit)


    payload = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"'+deviceID+'","treatment":{"instructions":[{"type":"OUTPUT","port":"CONTROLLER"}]},"selector":{"criteria":[{"type": "ETH_TYPE","ethType": "0x800"},{"type":"IPV4_SRC","ip":"'+destipv4+'"}]}}'
    jsonpayload = json.dumps(payload)
    jsonpayload = json.loads(payload)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=jsonpayload)
 
    status = (response.status_code) 
    print(status)

    flowid = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/application/{customID}'
    flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
    q = flowresponse.json()
    f=[]

    for i in q["flows"]:
        if i["deviceId"] == deviceID:
            flowid = i["id"]
            break


    avg = 0
    onos_url = f'http://localhost:8181/onos/v1/flows/{deviceID}/{flowid}'
    while avg < ratelimit:
        time.sleep(10)
        
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["bytes"]}'))
        print(f)
       
        Sum1 = sum(f)
        time.sleep(10)
        flowresponse = requests.get(onos_url, auth=(onos_username, onos_password))
        q = flowresponse.json()
        f=[]
        f.append(int(f'{q["flows"][0]["bytes"]}'))
        Sum2 = sum(f)
        
        avg = (Sum2 - Sum1)/10
        print(avg) 

    print(q["flows"][0]["treatment"]["instructions"][0])

    q["flows"][0]["treatment"]["instructions"][0] = {"type": "OUTPUT", "port": "DROP"}
    print(q["flows"][0])
    foo = (q["flows"][0])
    [foo.pop(x) for x in ["groupId","state","liveType","life","lastSeen","bytes","id", "appId","packets","tableId","tableName"]]
    
    var = '{"priority":40000,"timeout":0,"isPermanent":true,"deviceId":"of:00003c2c301b9c81","treatment":{},"selector":{"criteria":[{"type":"ETH_TYPE","ethType":"0x800"},{"type":"IPV4_SRC","ip":"'+destipv4+'"}]}}'
    data = json.dumps(var)
    data = json.loads(var)

    print(var)
    onos_url = f'http://localhost:8181/onos/v1/flows/{jsonpayload["deviceId"]}?appId={customID}'
    response = requests.post(onos_url, auth=(onos_username, onos_password), json=data)
    print(response)

    return redirect('/configure')