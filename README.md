# 2IC80-group12
Requires at least Python 3.5 with Scapy and NetfilterQueue

## ARP
In order to run the ARP poisoning, run the following command
``sudo python runARPPoisoning.py``

To get more information about the different parameters you can pass, run
``sudo python runARPPoisoning.py --help`` or ``sudo python runARPPoisoning.py -h``

## DNS
In order to run the DNS spoofing, run the following command
``sudo python runDNSResponseIntercept.py``

To get more information about the different parameters you can pass, run
``sudo python runDNSResponseIntercept.py --help`` or ``sudo python runDNSResponseIntercept.py -h``

Make sure the file with the DNS host mapping is in the same folder as the program (custom name can be given as argument).

## DNS without outside responses
This program is not yet working correctly and results in DNS queries of the victim until the program is stopped.

In order to run the DNS spoofing without outside responses, run the following command
``sudo python runDNSQueryIntercept.py``

To get more information about the different parameters you can pass, run
``sudo python runDNSQueryIntercept.py --help`` or ``sudo python runDNSQueryIntercept.py -h``

Make sure the file with the DNS host mapping is in the same folder as the program (custom name can be given as argument).
