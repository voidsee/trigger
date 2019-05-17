#!/usr/bin/python3
from scapy.all import *
from random import sample
conf.L3socket=L3RawSocket

def c_ping_dst(p):
        #p.show()
        #p[Ether].dst,p[Ether].src = p[Ether].src,p[Ether].dst
        if p[Ether].type == 0x806 and p[ARP].op==1:
                hs = ":".join(["".join(sample("0123456789abcdef",2)) for i in range(6)])
                #print(hs)
                a=Ether(dst=p[Ether].src)/ARP(psrc=p[ARP].pdst,hwdst=p[ARP].hwsrc, hwsrc=hs, pdst=p[ARP].psrc,hwlen=6,plen=4,op=2)
                sendp(a, iface="wlo1")
        elif p[Ether].type == 0x0800:
                if p[IP].dst in ip_list:
                        p[IP].dst,p[IP].src = p[IP].src,p[IP].dst
                        p[ICMP].type=0
                        del p[ICMP].chksum, p[IP].chksum
                        x = raw(p[IP])
                        p=IP(x)
                        send(p, iface="wlo1")
                        p.show()

def icmp_reply(ip_list, Iface="eth0"):
        sniff(iface=Iface, filter="icmp or arp", prn=c_ping_dst)

if __name__ == "__main__":
        ip_list=["192.168.123.129", "192.168.123.25"] 
        icmp_reply(ip_list, Iface="eno1")
        #icmp_reply(ip_list, Iface='wlo1')
