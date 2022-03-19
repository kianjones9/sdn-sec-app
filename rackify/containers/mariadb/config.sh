#!/bin/bash
apt get update
apt install iproute2
apt install iputils-ping

ip link set eth0 down
# get IP to remove
# IP=$(ip add | grep -o 192.168.[0-9]*.[0-9]*/24)

# networking config
# ip route del default 

# set bridge IP
# ip route add default via dev eth0

#ip addr add 172.17.$RACK_NUM.12/24 dev br0
#ip link set br0 up

# add default route
#ip route add default dev br0

#container config:
#       enable packet forwarding?