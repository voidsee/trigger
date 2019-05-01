#!/usr/bin/python3
from random import *


def get_ips(ip_file):
    with open(ip_file, "r") as fd:
        ips = fd.read().splitlines()
        #print(ips)
    return ips

def split_ips(ips):
    lnth = len(ips)
    if lnth > 2:
        rndm = randint(1, lnth//3)
        shuffle(ips)
        return ips[:rndm],ips[rndm:]
    elif lnth==2:
        return ips[:1],ips[1:]
    else:
        return None,ips
    
def gen_ports(ips, n):
    ip_ports = []
    for ip in ips:
        ports = ",".join([str(i) for i in sample(list(range(999, n + 2137)), n)])
        ip_ports.append([ip, ports])
    return ip_ports


def split_ports(ip_ports, n):
    shuffle(ip_ports)
    lnth = len(ip_ports)
    splited_ports=[]
    for i in range(n):
        splited_ports.append(ip_ports[i*lnth//n:(i+1)*lnth//n])
    return splited_ports
   
def gather_ports(ip_ports):
    ports=[]
    for i in ip_ports:
        ports.append(i[1])
    return ports
    


if __name__ == '__main__':
    import scan
    from pprint import pprint

    n = int(input("input number"))
    a, b = split_ips(get_ips("ips")); c = gen_ports(b, n); d = scan.filter(c); e,f =split_ports(d, 2);

    print("ips0");pprint(a); print("ips1");pprint(b); print("ip_ports");pprint(c);
    print("ip_ports not open");pprint(d); print("ip_ports0 not open");pprint(e); print("ip_ports1 not open");pprint(f);
##########################################################################################
    #ip_ports = [['172.17.0.1', 1584],
             #['220.181.112.244', 1530],
             #['202.89.233.101', 1307],
             #['220.181.112.244', 1749],
             #['172.17.0.1', 1506],
             #['202.89.233.101', 1700]]
    #pprint(split_ports(ip_ports,n))
    #print(gather_ports(ip_ports))

