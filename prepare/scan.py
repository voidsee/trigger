#!/usr/bin/python3
import sys
import nmap

def filter(ip_ports):
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        print(str(e))
        sys.exit(0)
    result=[]
    try:
        for ip_port in ip_ports:
            ip, port = ip_port
            nm.scan(ip, port, '-v -sS')
            print('------------------------------------------------------')#
            print('Host : %s (%s)' % (ip, nm[ip].hostname()))#
            print('State : %s' % nm[ip].state())#
            for proto in nm[ip].all_protocols():
                print('--------------')#
                print('Protocol : %s' % proto)#
                for port in sorted(list(nm[ip][proto].keys())):
                    print("scanning:",port)#
                    if nm[ip][proto][port]['state'] != "open":
                        result.append([ip, port])

        return result
    except Exception as e:
        print("Scan error:" + str(e))

if __name__ == "__main__":
    scan_rows = [("127.0.0.1", "80,3306,22,443"),("192.168.31.122", "80,443"),("10.177.53.160", "80,3306,22,443")]
    print(filter(scan_rows))

