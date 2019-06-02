#!/usr/bin/python3
import pymysql.cursors
from sys import exit

class Up_Score:
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
                    elif line[0]=='[score]':
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
    #########################################################################################
    def insert_score(self, score): 
        """insert score to database"""
        try:
            self.clear_table()
            with self.conn.cursor() as cursor:
                sql_insert = "insert into {} values({},{},{},{});"\
                        .format(self.task_name, score[0],score[1],score[2],score[3])
                cursor.execute(sql_insert)
                self.conn.commit()
                print("success...")
        except:
            print("mysql error:insert table")

    def clear_table(self, ):   # find the TASK's strategy
        """clear the given table"""
        try:
            with self.conn.cursor() as cursor:
                sql_get = "truncate {};".format(self.task_name)
                cursor.execute(sql_get)
                self.conn.commit()
        except:
            print("mysql error:clear table")


if "__main__" == __name__:
    from pprint import pprint
    us = Up_Score()
