#!/usr/bin/python3
import pymysql.cursors
from sys import exit

class DB:
    def __init__(self,):
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
                    elif line[0]=='[strategy]':
                        self.task_name = line[1]
                        #break
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
    #########################################################################################
    def insert_strategy(self, IP, flag, PORT=0, SRV='None'): 
        """insert ip,[port,[service,]] to database"""
        try:
            with self.conn.cursor() as cursor:
                sql_insert = "insert into {} values('{}',{},{},'{}');"\
                        .format(self.task_name,IP,flag,PORT,SRV)
                print("success:",sql_insert)
                cursor.execute(sql_insert)
                self.conn.commit()
        except:
            print("mysql error:insert table")


    def insert_t1(self, ips):  
        """only ip"""
        for i in ips:
            self.insert_strategy(IP=i, flag=1)
    def insert_t2(self, ip_ports):
        """ip and port"""
        for i in ip_ports:
            self.insert_strategy(IP=i[0], flag=2, PORT=i[1])
    def insert_t3(self, ip_port_srv):
        """ip port and service"""
        for i in ip_port_srv:
            self.insert_strategy(IP=i[0], flag=3, PORT=i[1], SRV=i[2])

    def insert_all(self, ips, ip_ports, ip_port_srv):
        self.insert_t1(ips)
        self.insert_t2(ip_ports)
        self.insert_t3(ip_port_srv)

    ########################################################################################
    def split_table(self, ):
        """split table into ip, ip:port, ip:port:service by flag"""
        self.get_table()
        ips=[]; ip_ports=[]; ip_port_srv=[];
        for row in self.table:
            if row[1]==1:
                ips.append(row[0])
            elif row[1] == 2:
                ip_ports.append([row[0], row[2]])
            else:
                ip_port_srv.append([row[0], row[2], row[3]])
        return [ips, ip_ports, ip_port_srv]

    def get_table(self, ):   # find the TASK's strategy
        """pull the table from database"""
        try:
            with self.conn.cursor() as cursor:
                sql_get = "select * from {};".format(self.task_name)
                cursor.execute(sql_get)
                self.table = cursor.fetchall()
            return self.table
        except:
            print("mysql error:get table")

    ########################################################################################
    def clear_table(self, ):   # find the TASK's strategy
        """clear the given table"""
        try:
            with self.conn.cursor() as cursor:
                sql_clear = "truncate {};".format(self.task_name)
                cursor.execute(sql_clear)
                print("clear table[{}] success!".format(self.task_name))
        except:
            print("mysql error:clear table")
    ########################################################################################

if "__main__" == __name__:
    from pprint import pprint
    db = DB()
    #db.clear_table()

    #ips = ['192,168.31.127', '127.0.0.1']
    #ip_ports = [['192.168.31.127',22], ['192.168.31.127',22], ['127.0.0.1',3306]]
    #ip_port_srv = [['192.168.31.127', 443, 'https'], ['192.168.31.127', 8080, 'nginx']]
    #db.insert_all(ips, ip_ports, ip_port_srv)

    data = db.get_table()
    pprint(data)
    print()
    a, b, c = db.split_table()
    pprint(a); pprint(b); pprint(c)

    
