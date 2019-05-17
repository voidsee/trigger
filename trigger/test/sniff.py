#!/usr/bin/python3
from scapy.all import *


def tmp(p):
	if p[IP].dst=="12.12.12.12":#a->b
		p.show()
		p[IP].dst, p[IP].src=p[IP].src, p[IP].dst
		sendp(p)
	
	#if p[IP].dst=="10.0.3.88":#a->b
		#p[IP].dst="192.168.31.205"#a->c
		#sendp(p)
		#p.show()
	#if p[IP].dst=="192.168.220.129":#c->a
		#p[IP].src="10.0.3.88"#b->a
		#p.show()

pkt = sniff(iface="ens33",filter="icmp",count = 50,prn=tmp)
print("over")
