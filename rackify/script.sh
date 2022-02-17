#!/bin/bash

# OVS config:
# remove int IPs
ip add del 172.17.0.0/16 dev eth0

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
ip addr add 172.17.10.12/24 dev br0
ip link set br0 up

#container config:
#       enable packet forwarding?
