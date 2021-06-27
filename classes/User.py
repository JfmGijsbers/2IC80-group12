from scapy.all import *
from getmac import get_mac_address as gma

class User:
    def __init__(self, IP, MAC = ""):
        self.IP = IP
        self.MAC = MAC

    def get_mac(self):
        print(getmacbyip(self.IP))
        self.MAC = getmacbyip(self.IP)
        if (self.MAC) == "ff:ff:ff:ff:ff:ff":
            self.MAC = gma()
            print(gma())

    def set_mac(self, MAC):
        self.MAC = MAC