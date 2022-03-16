#!/bin/bash

# get IP to remove
IP=$(ip add | grep -o 172.17.[0-9]*.[0-9]*/16)

# OVS config:
# remove int IPs
ip add del $IP dev eth0
ip add del $IP dev eth1

# add a bridge
ovs-vsctl add-br br0

# add ints to br
ovs-vsctl add-port br0 eth0

# config controller IP
ovs-vsctl set-controller br0 tcp:10.43.1.10:6653

# config OF protocols
ovs-vsctl set bridge br0 protocols=OpenFlow10,OpenFlow13

# set bridge IP
ip addr flush dev eth0
ip addr add 172.$SERVER_ID.$RACK_NUM.12/24 dev br0
ip link set br0 up

# add default route
ip route add default dev br0

#container config:
#       enable packet forwarding?