#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.append('../prepare/')
from conn_db import get_table,split_table
from pprint import pprint

TASK_NAME = "A"

table = get_table(TASK_NAME)
pprint(table)

a,b,c = split_table(table)
print(a)
print(b)
print(c)
