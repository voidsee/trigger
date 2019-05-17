#!/usr/bin/python3
# coding=utf-8

from scapy.all import *
conf.L3socket=L3RawSocket
from pprint import pprint
def c_ping_dst(p):
        if p[ARP].pdst in ip_list:
            p.show2()
            #p[Ether].dst,p[Ether].src = p[Ether].src,p[Ether].dst
            #a=Ether(dst=p[Ether].src)/ARP(psrc=p[ARP].pdst,hwdst=p[ARP].hwsrc, pdst=p[ARP].psr)
            a=Ether(dst=p[Ether].src,src="c8:21:58:2e:13:8c")/ARP(psrc=p[ARP].pdst,hwdst=p[ARP].hwsrc, hwsrc="c8:21:58:2e:13:8c", pdst=p[ARP].psrc,hwlen=6,plen=4,op=2)
            a.show2() 
            sendp(a, iface="wlo1")
def icmp_reply(ip_list, Iface="eth0"):
        sniff(iface=Iface, filter="arp", prn=c_ping_dst)

if __name__ == "__main__":
        ip_list=["192.168.123.129", "192.168.123.25"] 
        #icmp_reply(ip_list, Iface="eno1")
        icmp_reply(ip_list, Iface='wlo1')
