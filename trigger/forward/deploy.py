#!/usr/bin/env python
# coding=utf-8
import multiprocessing
from time import sleep
import signal
from mk_packet import Packet
from dkr_rspns import Iptb
import sys
sys.path.append("../prepare")
from conn_db import DB

TASK_NAME="A"
db = DB(TASK_NAME)
ips, ip_ports, ip_port_srv = db.split_table()
#####################
#ips=["192.168.123.24",]
#ip_ports=[["192.168.123.25", 99],]
#ip_port_srv=[["192.168.31.26", 3307, "mysql"],]
print(ips, ip_ports, ip_port_srv, sep="\n")
#####################
def exit(signum, frame):
    dk.clr_ips()
    dk.clr_white_list()
    #print("exit")
    sys.exit()
signal.signal(signal.SIGINT, exit)


rp = Packet(ips, ip_ports)
tb = Iptb(ip_port_srv, "wlo1")
tb.set_ips(); tb.set_white_list()


icmp = multiprocessing.Process(target=rp.reply,\
        args=("icmp or arp", "wlo1",rp.arp_icmp))
tcp = multiprocessing.Process(target=rp.reply,\
        args=("tcp or arp", "wlo1",rp.arp_tcp))
icmp.daemon=True; tcp.daemon=True

duration = int(input("run time(min) = "))*60
icmp.start(); tcp.start()
sleep(duration)

tb.clr_ips(); tb.clr_white_list()

if __name__ == "__main__":
    print("test over.")
