#!/usr/bin/env python
# coding=utf-8
from scapy.all import *
from random import sample
import sys
sys.path.append("../prepare")
from split import Ip_op

class Packet:
    conf.L3socket=L3RawSocket
    def __init__(self, ips=[], ip_ports=[], show=False):
        self.ip_ports=ip_ports
        self.ips=ips
        self.show=show
            
    def mk_arp(self, p, ips):
        if p[Ether].type == 0x806 and p[ARP].op==1 and p[ARP].pdst in ips:
            mac = ":".join(["".join(sample("0123456789abcdef",2)) for i in range(6)])
            rspn = Ether(dst=p[Ether].src)\
                    /ARP(psrc=p[ARP].pdst,hwdst=p[ARP].hwsrc, hwsrc=mac, pdst=p[ARP].psrc,hwlen=6,plen=4,op=2)
            sendp(rspn, iface="wlo1")
            if self.show:
                rspn.show2()### 

    def mk_icmp(self, p):
        if  p[Ether].type == 0x0800 and p[IP].dst in self.ips:
            p[IP].dst,p[IP].src = p[IP].src,p[IP].dst
            p[ICMP].type=0; del p[ICMP].chksum, p[IP].chksum
            rspn = IP(raw(p[IP]))
            send(rspn, iface="wlo1")
            if self.show:
                rspn.show()###

    def mk_tcp(self, p):
        for ip_port in self.ip_ports:
            if p[Ether].type == 0x0800 and p[IP].dst == ip_port[0] and p[TCP].dport == ip_port[1]:
                if p[TCP].flags == 'S':
                    rspn= IP(src=p[IP].dst, dst=p[IP].src)/\
                        TCP(sport=p[TCP].dport,dport=p[TCP].sport,seq=p[TCP].seq,flags="SA",ack=p[TCP].seq+1)
                    send(rspn,iface="wlo1")
                    rspn.show()###
                elif p[TCP].flags == 'A':
                    rspn= IP(src=p[IP].dst, dst=p[IP].src)/\
                        TCP(sport=p[TCP].dport,dport=p[TCP].sport,seq=p[TCP].seq,flags="RA",ack=1)
                    send(rspn,iface="wlo1")
                    if self.show:
                        rspn.show()###
                break

    def arp_icmp(self, p):
        self.mk_arp(p, self.ips)
        self.mk_icmp(p)
    def arp_tcp(self, p):
        ip_op=Ip_op()
        ips = ip_op.gather_ips(self.ip_ports)
        self.mk_arp(p, ips)
        self.mk_tcp(p)

    def reply(self, rule, iface="eth0", match=lambda p: p.show()):
        sniff(iface=iface, filter=rule, prn=match)

if __name__ == "__main__":
    ip_ports=[["192.168.123.129",80], ["192.168.123.27",8080], ["192.168.123.202",8280]]
    ips=["192.168.123.129", "192.168.123.24", "192.168.123.25", "192.168.123.26"] 
    rp = Packet(ips, ip_ports, show=True)
    n = input("input q, 1, 2: ")
    while len(n)!=0 and n[0]!="q":
        if n[0]=="1":
            rp.reply("icmp or arp", "wlo1", rp.arp_icmp)
        else:
            rp.reply("tcp or arp", "wlo1", rp.arp_tcp)
        n = input("input q, 1, 2: ")

