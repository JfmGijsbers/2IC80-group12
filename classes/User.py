from scapy.all import *

class User:
    def __init__(self, IP, MAC = ""):
        self.IP = IP
        self.MAC = MAC

    def get_mac(self):
        print(getmacbyip(self.IP))
        self.MAC = getmacbyip(self.IP)
        if (self.MAC) == "ff:ff:ff:ff:ff:ff":
            self.MAC = ""
            print(f"FATAL ERROR: could not find MAC for IP {self.IP}")

    def set_mac(self, MAC):
        self.MAC = MAC