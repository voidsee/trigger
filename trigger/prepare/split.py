#!/usr/bin/python3
from random import *

class Ip_op:
    def __init__(self, ips=["127.0.0.1",]):
        self.ips = ips

    def get_ips(self, ip_file):
        """get ip list from file"""
        with open(ip_file, "r") as fd:
            self.ips = fd.read().splitlines()
        return self.ips
        
    def gen_ports(self, ips, n=2):
        """[ip,] => [[ip,'port1,port2,'],]"""
        ip_ports = []
        for ip in ips:
            ports = ",".join([str(i) for i in sample(list(range(3999, n+7137)), n)])
            ip_ports.append([ip, ports])
        return ip_ports

    def cat_ip(self, ip, num):
        """ip=1.1.1.1 + num=5 => return 1.1.1.5"""
        return ".".join(ip.split(".")[:-1])+"."+str(num)
    def pick_ips(self,):
        """ pick ip out of ips but in same net"""
        ips_a=[]
        if 0<len(self.ips)<254:
            while True:
                i = choice(list(range(2,255)))
                ip = self.cat_ip(self.ips[0],i)
                if not ip in self.ips :
                   ips_a.append(ip) 
                   if len(ips_a)>=(len(self.ips)+5)//6:
                       break
        return ips_a
    def depart_ports(self, ip_ports):
        """ [[ip,'port1,port2,'],] => [[ip,port1],[ip,port2]] """
        result = []
        for ip_port in ip_ports:
            for port in ip_port[1].split(','):
                if random()<0.7:
                    result.append([ip_port[0],int(port)])
        return result

    def gen_dk_ports(self,):
        """ generate some ip:port for docker"""
        ips_a = self.pick_ips()
        ip_ports = self.gen_ports(ips_a, n=2)
        return self.depart_ports(ip_ports)

    ############################################################
    def split_ips(self, ips):
        """split ips into 2 parts"""
        lnth = len(ips)
        if lnth > 2:
            shuffle(ips)
            return ips[:lnth//3],ips[lnth//3:]
        elif lnth==2:
            return ips[:1],ips[1:]
        else:
            return [],ips
    ############################################################

    def split_ports(self, ip_ports, n=2,):
        """split [[ip,port],...] into n parts """
        shuffle(ip_ports)
        lnth = len(ip_ports)
        if lnth >= n:
            splited_ports=[]
            for i in range(n):
                splited_ports.append(ip_ports[i*lnth//n:(i+1)*lnth//n])
            return splited_ports
        else:
            return ip_ports
       
    def gather_ports(self, ip_ports):
        """[[ip1,port1],[ip2,port2]] => [port1,port2]"""
        ports=[]
        for ip_port in ip_ports:
            if not ip_port[1] in ports: 
                ports.append(ip_port[1])
        return ports
    def gather_ips(self, ip_ports):
        """[[ip1,port1],[ip2,port2]] => [ip1,ip2]"""
        ips=[]
        for ip_port in ip_ports:
            if not ip_port[0] in ips:
                ips.append(ip_port[0])
        return ips


if __name__ == '__main__':
    from scan import Filter
    from pprint import pprint

    ip_op = Ip_op();ip_op.get_ips("ips")
    a = ip_op.gen_ports(ip_op.ips, 3)
    print(ip_op.ips);print("ip add ports: ");pprint(a)
    filter=Filter(ip_op.ips, a)
    ips = filter.scan_ips()
    ip_ports = filter.scan_ports()
    print("ips down for icmp: ",ips)
    print("ip_ports not open for tcp: ");pprint(ip_ports)
    ip_port_srv = ip_op.gen_dk_ports()
    print("ip_ports for docker: ");pprint(ip_port_srv)
    print("ip for docker: ");pprint(ip_op.gather_ips(ip_port_srv))
    print("ports for docker: ");pprint(ip_op.gather_ports(ip_port_srv))
    print("split ports of ip_ports: ");pprint(ip_op.split_ports(ip_ports))

