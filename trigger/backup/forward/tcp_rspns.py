#!/usr/bin/python3
from scapy.all import *
from random import sample
conf.L3socket=L3RawSocket

def c_tcp_dst(p):
    if p[Ether].type == 0x806 and p[ARP].op==1:
    #if p[Ether].type == 0x806 and i==0:
        hs = ":".join(["".join(sample("0123456789abcdef",2)) for i in range(6)])
        a=Ether(dst=p[Ether].src)/ARP(psrc=p[ARP].pdst,hwdst=p[ARP].hwsrc, hwsrc=hs, pdst=p[ARP].psrc,hwlen=6,plen=4,op=2)
        sendp(a, iface="wlo1")
    elif p[Ether].type == 0x0800:
        for ip_port in ip_list:
            if p[IP].dst == ip_port[0] and p[TCP].dport == ip_port[1]:
                if p[TCP].flags == 'S':
                    p.show()###
                    x= IP(src=p[IP].dst, dst=p[IP].src)/\
                        TCP(sport=p[TCP].dport,dport=p[TCP].sport,seq=p[TCP].seq,flags="SA",ack=p[TCP].seq+1)
                    send(x,iface="wlo1")
                elif p[TCP].flags == 'A':
                    p.show()###
                    x= IP(src=p[IP].dst, dst=p[IP].src)/\
                        TCP(sport=p[TCP].dport,dport=p[TCP].sport,seq=p[TCP].seq,flags="RA",ack=1)

            

def tcp_reply(ip_list, Iface="eth0"):
    sniff(iface=Iface, filter="tcp or arp", prn=c_tcp_dst)

if __name__ == "__main__":
    ip_list=[["192.168.123.129",80], ["192.168.123.27",8080], ["192.168.123.202",8280]]
    tcp_reply(ip_list, Iface="eno1")
    #icmp_reply(ip_list, Iface='wlo1')
