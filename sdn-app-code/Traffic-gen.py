import sys
from scapy.all import Ether,IP,TCP, sendpfast

if sys.argv[1] == "--help":
    print("\nCorrect formatting is:\n\tpython3 Capstone-scapy.py 'type of demo: PPS, HTTP' 'Dst IP address' 'SRC IP address'\n")

elif sys.argv[1] == "HTTP":
    #Specify what IP you want when running the script
    pkt = Ether()/IP(dst=sys.argv[2],src=sys.argv[3])/TCP(sport=80,dport=80)/"GET /index.html HTTP/1.0"#Demo Data"
    #pps is how many packet you want per second, 
    #loop is how long you want to run it with each 1 second = pps x 10
    sendpfast(pkt, pps=1000, loop=10000)

elif sys.argv[1] == "PPS":
    #Specify what IP you want when running the script
    pkt = Ether()/IP(dst=sys.argv[2],src=sys.argv[3])/TCP()/"#Demo Data"
    #pps is how many packet you want per second, 
    #loop is how long you want to run it with each 1 second = pps x 10
    sendpfast(pkt, pps=1000, loop=10000)

elif sys.argv[1] == "BW":
    #Will output 500mbps to dst for 10 seconds
    pkt = Ether()/IP(dst=sys.argv[2],src=sys.argv[3])/TCP()/"zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz" 
    # PPS 2000 = 1 mpbs
    # loop is how long you want to run it with each 1 second = pps x 10
    sendpfast(pkt, pps=200000, loop=2000000)