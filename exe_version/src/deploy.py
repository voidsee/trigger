#!/usr/bin/env python
# coding=utf-8
import multiprocessing
from time import sleep
import signal
from sys import exit
from mk_packet import Packet
from dkr_rspns import Iptb
from conn_db import DB
from up_pks import up_load_ip_dict


def deploy(iface="eth0",):
    multiprocessing.freeze_support()
    db = DB()
    ips, ip_ports, ip_port_srv = db.split_table()

    rp = Packet(ips, ip_ports, True)
    tb = Iptb(ip_port_srv, "wlo1")
    tb.set_ips(); tb.set_white_list()

    def exit_this(signum, frame):
        tb.clr_ips()
        tb.clr_white_list()
        #print("exit")
        #up_load_ip_dict()################
        exit()
    signal.signal(signal.SIGINT, exit_this)

    icmp = multiprocessing.Process(target=rp.reply,\
            args=("icmp or arp", iface, rp.arp_icmp))
    tcp = multiprocessing.Process(target=rp.reply,\
            args=("tcp or arp", iface, rp.arp_tcp))
    icmp.daemon=True; tcp.daemon=True

    duration = int(input("run time(min) = "))*60
    icmp.start(); tcp.start()
    sleep(duration)

    tb.clr_ips(); tb.clr_white_list()
    #up_load_ip_dict()################

if __name__ == "__main__":
    deploy("eno1")
    print("test over.")
