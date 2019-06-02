#!/usr/bin/python3
import sys
import nmap
from random import random,shuffle

class Filter:
    def __init__(self, ips=[], ip_ports=[],show=True):
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print('Nmap not found', sys.exc_info()[0])
            sys.exit(0)
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            print(str(e))
            sys.exit(0)
        self.ips = ips
        self.ip_ports = ip_ports
        self.scale = 0.7
        self.show = show

    def scan_ips(self,):
        result=[]
        shuffle(self.ips)
        try:
            if self.show:
                print("################## scanning ip ####################")
            for ip in self.ips:
                self.nm.scan(hosts=ip, arguments='-v -sn')
                if self.show:
                    print('------------------------------------------------------')#
                    print('Host : %s (%s)' % (ip, self.nm[ip].hostname()))#
                    print('State : %s' % self.nm[ip].state())#
                if self.nm[ip].state()=='down':
                    result.append(ip)
                    if len(result) > len(self.ips)//2 :
                        break
            return result

        except Exception as e:
            print("Scan error:" + str(e))

    def scan_ports(self,):
        """if the port not open or the host is down, join the result"""
        result=[]
        try:
            if self.show:
                print("################## scanning port ####################")
            for ip_port in self.ip_ports:
                ip, port = ip_port
                self.nm.scan(ip, port, '-v -sS')
                if self.show:
                    print('------------------------------------------------------')#
                    print('Host : %s (%s)' % (ip, self.nm[ip].hostname()))#
                    print('State : %s' % self.nm[ip].state())#
                if self.nm[ip].state()=='down':
                    for port in ip_port[1].split(','):
                        if random()<self.scale:
                            result.append([ip_port[0],int(port)])
                        elif not len(result):
                            result.append([ip_port[0],int(port)])
                else:
                    for port in sorted(list(self.nm[ip]['tcp'].keys())):
                        if self.show:
                            print("scanning:",port)#
                        if self.nm[ip]['tcp'][port]['state'] != "open":
                            result.append([ip, port])

            return result
        except Exception as e:
            print("Scan error:" + str(e))

if __name__ == "__main__":
    from pprint import pprint
    scan_rows = [("127.0.0.1", "80,3306,22,443"),("192.168.31.122", "80,443"),("10.177.53.160", "80,3306,22,443"),("192.168.123.129","23,45,667")]
    ips = ["127.0.0.1", "8.8.8.8", "192.168.123.129"]

    ftr=Filter(ips, ip_ports = scan_rows)
    x=ftr.scan_ports()
    pprint(x)
    print("##############################")
    x= ftr.scan_ips()
    print(x)

