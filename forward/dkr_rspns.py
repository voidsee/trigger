#!/usr/bin/python3
from scapy.all import *

def c_tcp(p):
	for ip_port in ip_ports_list:
		if p[IP].dst==ip_port[0] and str(p[TCP].dport) in ip_port[1].split(","):
			print("before ", p[IP][TCP].dport);p.show()
			p[IP].dst="localhost"
			#sendp(p)
			send(p[IP])
			print("after ", p[IP][TCP].dport);p.show()
			break
	#if p[IP].src == "192.168.220.129":
		#p[IP].src == current_ip
		#p[IP].src = "12.12.12.12"
		#sendp(p)

def tcp_reply(ip_ports_list, Iface="eth0"):
	#ips = [i[0] for i in ip_ports_list]
	#ports = [i[1] for i in ip_ports_list]
	sniff(iface=Iface, filter="tcp", prn=c_tcp)

if __name__ == "__main__":
	ip_ports_list=[["10.0.3.88", "22,99,3306"], ["12.12.12.12", "80,5382,7080,3307"]]
	tcp_reply(ip_ports_list, Iface="ens33")
