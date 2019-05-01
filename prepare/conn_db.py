#!/usr/bin/python3

import pymysql.cursors

TASK_NAME = "A"


def mysql_connect():
    conn= pymysql.connect(
        host="127.0.0.1",
        user="guest",
        password="guest",
        db="guest",
        charset="utf8"
    )
    return conn

#########################################################################################
def insert_strategy(IP, flag, PORT='None', SRV='None'):  # IP字符串，port 整数，docker 字符串， flag整数
    try:
        conn= mysql_connect()
        with conn.cursor() as cursor:
            sql_insert = "insert into {}_strategy values('{}',{:d},'{:d}','{}');".format(TASK_NAME,IP,flag,PORT,SRV)
            print("success:",sql_insert)
            cursor.execute(sql_insert)
            conn.commit()
    except:
        print("mysql error")


def insert_t1(ips):  # 传入的是只有IP的表，其余都是空
    for i in ips:
        insert_strategy(IP=i, flag=1)
def insert_t2(ip_ports):  # 传入的是IP-PORT的表
    for i in ip_ports:
        insert_strategy(IP=i[0], flag=2, PORT=i[1])
def insert_t3(ip_port_srv):
    for i in ip_port_srv:
        insert_strategy(IP=i[0], flag=3, PORT=i[1], SRV=i[2])

def insert_all(ips, ip_ports, ip_port_srv):
    insert_t1(ips)
    insert_t2(ip_ports)
    insert_t3(ip_port_srv)

########################################################################################
def split_table(table):
    ips=[]; ip_ports=[]; ip_port_srv=[];
    for row in table:
        if row[1]==1:
            ips.append(row[0])
        elif row[1] == 2:
            ip_ports.append([row[0], row[2]])
        else:
            ip_port_srv.append([row[0], row[2]])
    return ips, ip_ports, ip_port_srv

def get_table(task_name):   # find the TASK's strategy
    try:
        conn = mysql_connect()
        with conn.cursor() as cursor:
            sql_get = "select * from {}_strategy;".format(task_name)
            cursor.execute(sql_get)
            table = cursor.fetchall()
            if table:
                if table[0]:
                    return table
    except:
        print("mysql error")

########################################################################################
def clear_table(task_name):   # find the TASK's strategy
    try:
        conn = mysql_connect()
        with conn.cursor() as cursor:
            sql_get = "truncate {}_strategy;".format(task_name)
            cursor.execute(sql_get)
            print("clear table[{}_strategy] success!".format(task_name))
            
    except:
        print("mysql error")
########################################################################################

if "__main__" == __name__:
    from pprint import pprint

    clear_table(TASK_NAME)

    ips = ['192,168.31.127', '127.0.0.1']
    ip_ports = [['192.168.31.127','22'], ['192.168.31.127','22'], ['127.0.0.1','3306']]
    ip_port_srv = [['192.168.31.127', '443', 'https'], ['192.168.31.127', '8080', 'nginx']]
    insert_all(ips, ip_ports, ip_port_srv)

    data = get_table(TASK_NAME)
    pprint(data)
    print()
    a, b, c = split_table(data)
    pprint(a); pprint(b); pprint(c)

    
