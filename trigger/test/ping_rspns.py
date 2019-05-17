#!/usr/bin/python3
from scapy.all import *
conf.L3socket=L3RawSocket
def c_ping_dst1(p):
        if p[IP].dst in ip_list:
                p.show2()
                ####p[IP].dst="localhost"
                x = IP(dst="localhost",src=p[IP].src)/p[IP][ICMP]
                x.show2()
                send(x)
        if p[IP].src == "127.0.0.1":
                x = IP(dst=p[IP].dst,src="12.12.12.12")/p[IP][ICMP]
                x[ICMP].type = "echo-reply"
                x.show2()
                send(x)

def c_ping_dst(p):
        if p[IP].dst in ip_list:
                p[IP].dst,p[IP].src = p[IP].src,p[IP].dst
                send(p[IP])

def icmp_reply(ip_list, Iface="eth0"):
        sniff(iface=Iface, filter="icmp", prn=c_ping_dst1)

if __name__ == "__main__":
        ip_list=["10.0.3.88", "12.12.12.12", "192.168.123.129"] 
        #icmp_reply(ip_list, Iface="eno1")
        icmp_reply(ip_list, Iface='eno1')
