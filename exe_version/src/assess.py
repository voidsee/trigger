#!/usr/bin/env python
# coding=utf-8
from conn_db import DB
from evaluation import Evaluate
from bad_points import Neg
from pprint import pprint
from up_score import Up_Score


def assess(report, ip_file="ips",):
    db = DB()
    table = db.split_table()
    eva = Evaluate([2,5,3], [-1,-2],[0.9,0.8,0.6])
    eva.get_table(table)
    rpt = eva.get_report(report)

    if rpt:
        neg = Neg(table, ip_file)
        eva.bad_points(neg.bad_table())
        score = eva.stat()
        us = Up_Score()
        us.insert_score(score)

        #print("table:");pprint(table)
        #print("report:");pprint(rpt)
        #print("bad table:");pprint(neg.bad_table())
        #print(score)
        return score

if __name__ == "__main__":
    score = assess("report")
    print(score)
