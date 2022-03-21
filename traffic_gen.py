import sys
from scapy.all import Ether,IP,TCP, sendpfast

if sys.argv[1] == "--help":
    print("\nCorrect formatting is:\n\tpython3 Capstone-scapy.py 'Dst IP address' 'SRC IP address'\n")

else:
    #Specify what IP you want when running the script
    pkt = Ether()/IP(dst=sys.argv[1],src=sys.argv[2])/TCP()/"Demo Data"
    #pps is how many packet you want per second, 
    #loop is how long you want to run it with each 1000 = 1 second
    sendpfast(pkt, pps=1000, loop=10000)