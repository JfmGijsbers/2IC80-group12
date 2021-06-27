class User:
    def __init__(self, IP):
        self.IP = IP

    def get_mac(self):
        arp_req_frame = scapy.ARP(pdst = self.ip)
        broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
        self.MAC = answered_list[0][1].hwsrc
        return answered_list[0][1].hwsrc

    def set_mac(self, MAC):
        self.MAC = MAC