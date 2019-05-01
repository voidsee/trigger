#!/usr/bin/python3
from scapy.all import *

def c_ping_dst(p):
	if p[IP].dst in ip_list:
		p.show()
		print("hello")
		p[IP].dst="localhost"
		sendp(p)

def icmp_reply(ip_list, Iface="eth0"):
	sniff(iface=Iface, filter="icmp", prn=c_ping_dst)

if __name__ == "__main__":
	ip_list=["10.0.3.88", "12.12.12.12", "123.123.123.123"] 
	icmp_reply(ip_list, Iface="wlo1")
