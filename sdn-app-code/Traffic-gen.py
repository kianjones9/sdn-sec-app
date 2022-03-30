from asyncore import loop
import sys
from scapy.all import Ether,IP,TCP, sendpfast, ICMP, send

if sys.argv[1] == "--help":
    print("\nCorrect formatting is:\n\tpython3 Traffic-gen.py 'type of demo: PPS-1 or PPS-100' 'Dst IP address' 'SRC IP address'\n")
    print("PPS-1: PPS = 1pkt/s\nPPS-100: PPS = 100pkt/s\n\nPackets will be sent for 10 minutes or until Ctrl-C is pressed\n")

elif sys.argv[1] == "PPS-1":
    #PPS = 1pkt/s for 10mins or until Ctrl-C is pressed
    pkt=send(IP(dst=sys.argv[2],src=sys.argv[3])/ICMP(), count=600, inter=1)

elif sys.argv[1] == "PPS-100":
    #PPS = 100pkt/s for 10mins or until Ctrl-C is pressed
    pkt=send(IP(dst=sys.argv[2],src=sys.argv[3])/ICMP(), count=60000, inter=0.01)
