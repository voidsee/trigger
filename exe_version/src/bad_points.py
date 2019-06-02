#!/usr/bin/env python
# coding=utf-8
from split import Ip_op
from scan import Filter


class Neg:
    """generate ip and ip:port uesd for wrong report"""
    def __init__(self, table, ip_file="ips"):
        self.table = table
        self.get_ip_and_port(ip_file)

    def get_ip_and_port(self,ips):
        """pick ips from rest company ips and scan,
        generate ip:port list by gen_dk_ports([['ip',port],]) and scan"""
        ip_op = Ip_op()
        ip_op.get_ips(ips)
        ips_unscaned = ip_op.pick_ips(len(self.table[0])//2)
        ip_ports_int_unscaned = ip_op.gen_dk_ports(num=2,ip_n=len(self.table[1])//2)
        # ['ip',port] => ['ip','port']
        ip_ports_unscaned = []
        for i in ip_ports_int_unscaned:
            ip_ports_unscaned.append([i[0],str(i[1])])
        filter = Filter(ips_unscaned, ip_ports_unscaned,False)
        self.ips = filter.scan_ips()
        self.ip_ports = filter.scan_ports()

    def gen_n_ip(self, ):
        """if ip in not strategy table, include"""
        self.ips_a=[]
        for ip in self.ips:
            if not ip in self.table[0]:
                self.ips_a.append(ip)
        return self.ips_a

    def gen_n_ports(self, ):
        """if ip_ports not in strategy table, include"""
        self.ports_a=[]
        for port in self.ip_ports:
            if not port in self.table[1]:
                self.ports_a.append(port)
        return self.ports_a

    def bad_table(self,):
        self.gen_n_ip()
        self.gen_n_ports()
        return [self.ips_a,self.ports_a]


if __name__ == '__main__':
    from pprint import pprint
    
    table=[["12.12.12.12"],[["12.12.12.12",12],],[["12.12.12.12",12,"bug"]]]
    neg = Neg(table)
    print("ip:",neg.gen_n_ip())
    print("port:",neg.gen_n_ports())
    pprint(neg.bad_table())
