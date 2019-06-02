#!/usr/bin/env python
# coding=utf-8
from scapy.all import *
import pymysql.cursors
from sys import exit

class Up_Pcap:
    def __init__(self, ):
        self.mysql_connect()

    def mysql_connect(self,):
        try:
            with open(".dbconf","r") as dbf:
                line = dbf.readline().split()
                while line:
                    if line[0]=='[mysql]':
                        host = line[1]
                        user = line[2]
                        passwd = line[3]
                        db = line[4]
                    elif line[0]=='[ip_stat]':
                        self.task_name = line[1]
                    line = dbf.readline().split()

            self.conn=pymysql.connect(
                host=host,
                user=user,
                password=passwd,
                db=db,
                charset="utf8")
        except:
            print("mysql error, check <dbconf> file.")
            exit()

    def insert_sip(self, s_ip): 
        """insert score to database"""
        try:
            with self.conn.cursor() as cursor:
                for k,v in s_ip:
                    sql_insert = "insert into {} values('{}',{});"\
                            .format(self.task_name, k,v)
                    cursor.execute(sql_insert)
                self.conn.commit()
        except:
            print("mysql error:insert table")
    def insert_dip(self, d_ip): 
        """insert score to database"""
        try:
            with self.conn.cursor() as cursor:
                for k,v in d_ip:
                    sql_insert = "insert into {} values('{}',{});"\
                            .format(self.task_name, k,v)
                    cursor.execute(sql_insert)
                self.conn.commit()
        except:
            print("mysql error:insert table")

    def insert_both(self,ip_dict):
        self.insert_sip(ip_dict[0])
        self.insert_dip(ip_dict[1])
        
#########################################################################################

class DecodePcap:
    def __init__(self, pcap,):
        self.pks=rdpcap(pcap)

    def decode_sip(self,):
        s_ip={}
        for p in self.pks:
            if  p[Ether].type == 0x0800:
                s_ip[p[IP].src] = s_ip.get(p[IP].src,0)+1
            if p[Ether].type == 0x806:
                s_ip[p[ARP].psrc] = s_ip.get(p[ARP].psrc,0)+1
            #p.show()
        #print("src:");pprint(s_ip)
        return s_ip

    def decode_dip(self,):
        d_ip={}
        for p in self.pks:
            if  p[Ether].type == 0x0800:
                d_ip[p[IP].dst] = d_ip.get(p[IP].dst,0)+1
            if p[Ether].type == 0x806:
                d_ip[p[ARP].pdst] = d_ip.get(p[ARP].pdst,0)+1
            #p.show()
        #print("dst:");pprint(d_ip)
        return d_ip
    def decode(self,):
        sip=self.decode_sip()
        dip=self.decode_dip()
        return [sip,dip]
#########################################################################################

def up_load_ip_dict():
    dp = DecodePcap("receive_pks.pcap")
    up = Up_Pcap()

    ip_dict = dp.decode()
    #up.insert_both(ip_dict)
    #pprint(ip_dict)


if "__main__" == __name__:
    up_load_ip_dict()

