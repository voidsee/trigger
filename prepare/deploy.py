#!/usr/bin/env python
# coding=utf-8

from pprint import pprint
from split import *
import docker
from mng_docker import run_ctnrs
from conn_db import insert_all,clear_table
import scan

TASK_NAME = "A"

ip_file = 'ips'
n = int(input("input number"))

ips, ips2 = split_ips(get_ips(ip_file))
ip_ports0 = gen_ports(ips2, n)
ip_ports_ok = scan.filter(ip_ports0)
ip_ports,ip_ports1 =split_ports(ip_ports_ok , 2);
ip_port_srv = run_ctnrs(ip_ports1)

clear_table(TASK_NAME)
insert_all(ips, ip_ports, ip_port_srv)


if "__main__" == __name__:
    from conn_db import get_table
    table = get_table('A')
    pprint(table)
