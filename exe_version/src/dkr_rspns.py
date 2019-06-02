#!/usr/bin/python3
from os import system
from split import Ip_op

class Iptb:
    def __init__(self, ip_ports, iface="eth0"):
        ip_op = Ip_op()
        self.ip_ports = ip_ports
        self.ips = ip_op.gather_ips(ip_ports)
        self.iface=iface
        
    def set_ips(self,):
        for i in range(len(self.ips)):
            system("ifconfig {}:{} {}".format(self.iface, i, self.ips[i]))
    def clr_ips(self,):
        for i in range(len(self.ips)):
            system("ifconfig {}:{} down".format(self.iface, i,))

    def set_white_list(self,):
        system("iptables -tnat -NWHITE_LIST")
        system("iptables -tnat -IWHITE_LIST -ptcp -jDNAT --to 1.1.1.1")
        for i in range(len(self.ip_ports)):
            system("iptables -tnat -IWHITE_LIST -d{} -ptcp --dport {} -jDOCKER"\
                    .format(self.ip_ports[i][0], self.ip_ports[i][1]))
        system("iptables -tnat -IPREROUTING -jWHITE_LIST")
    def clr_white_list(self,):
        system("iptables -tnat -DPREROUTING -jWHITE_LIST")
        system("iptables -tnat -FWHITE_LIST")



if __name__ == "__main__":
    ip_ports=[["192.168.31.26", 3307], ["192.168.31.31", 7080]]
    dk = Iptb(ip_ports, "wlo1")
    n = input("input q ,1, 2:")
    while len(n)!=0 and n[0]!="q":
        if n[0]=="1":
            dk.set_ips()
            dk.set_white_list()
        else:
            dk.clr_white_list()
            dk.clr_ips()
        n = input("input q ,1, 2:")
