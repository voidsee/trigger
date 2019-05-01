#!/usr/bin/python3

with open("ips", 'w') as f:
    for k in range(31,32):
            for s in range(2,17):
                    print("192.168.%d.%d" % (k,s), file=f)
