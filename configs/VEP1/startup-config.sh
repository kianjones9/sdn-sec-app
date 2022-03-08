ip addr flush dev enp2s0f1
ip addr flush dev enp2s0f2
ip addr flush dev enp2s0f3

ip addr add 10.43.1.115/24 dev br0
ip link set dev br0 up
ip link set dev enp2s0f1 up
ip link set dev enp2s0f2 up
ip link set dev enp2s0f3 up

# add routing
# ip route add 10.43.1.0/24 dev br0
# ip route add 172.17.0.0/16 dev enp2s0f2

# add a bridge
ovs-vsctl add-br br0

# add ints to br
ovs-vsctl add-port br0 enp2s0f1
ovs-vsctl add-port br0 enp2s0f2
ovs-vsctl add-port br0 enp2s0f3

# config controller IP
ovs-vsctl set-controller br0 tcp:10.43.1.10:6653

# config OF protocols
ovs-vsctl set bridge br0 protocols=OpenFlow10,OpenFlow13
