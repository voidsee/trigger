#!/usr/bin/env python
# coding=utf-8

from pprint import pprint
#import docker
from split import Ip_op
from run_dks import Dkr
from conn_db import DB
from scan import Filter



def get_ready(ip_file,):
    #new Ip_op obj, init with ip_file
    ip_op = Ip_op();ip_ret = ip_op.get_ips(ip_file)
    if ip_ret:
        #generate ports on ip
        ip_ports_unscaned = ip_op.gen_ports(ip_op.ips, 3)
        #new filter obj, init with ips and unscaned ip:ports
        filter = Filter(ip_op.ips, ip_ports_unscaned)
        #get down ips and not opend ip:ports
        ips = filter.scan_ips(); ip_ports = filter.scan_ports()

        #generate ip:ports for docker
        ip_ports_dk = ip_op.gen_dk_ports()
        #new Dkr obj, init with ip:ports
        dkr = Dkr(ip_ports_dk)
        #run docker and get ip:port:srv
        ip_port_srv = dkr.run_ctnrs()

        db = DB()
        db.clear_table()
        db.insert_all(ips, ip_ports, ip_port_srv)


if "__main__" == __name__:
    ip_file = 'ips';
    get_ready(ip_file,)

    db = DB()
    pprint(db.get_table())
