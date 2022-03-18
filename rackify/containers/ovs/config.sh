#!/bin/bash

ip link set eth0 down

# OVS config
ovs-vsctl add-br br0
ovs-vsctl set-controller br0 tcp:10.43.1.10:6653
ovs-vsctl set bridge br0 protocols=OpenFlow10,OpenFlow13

ip addr add 172.$SERVER_ID.$RACK_NUM.12/24 dev br0
ip link set br0 up

# add default route
ip route add default dev br0