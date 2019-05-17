import sys
import nmap
from gen_ip_ports import *
# scan_rows = [("192.168.80.133", "80,443"),("192.168.123.127", "80")]
#scan_rows = [["192.168.123.127", "80,110"], ["192.168.123.127", "443"]]

def my_scan(strategy_list):
    result_rows = []
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except Exception as e:
        print("Unexpected error:", sys.exc_info()[0])
        print(str(e))
        sys.exit(0)
    promt)
    try:
        # 调用扫描方法，参数指定扫描主机hosts，nmap扫描命令行参数arguments
        for scan_row in strategy_list:
            hosts = scan_row[0]
            port = scan_row[1]
            nm.scan(hosts=hosts, arguments=' -v -sS -p ' + port)
            for host in nm.all_hosts():
                #print('------------------------------------------------------')
                # 输出主机及主机名
                #print('Host : %s (%s)' % (host, nm[host].hostname()))
                # 输出主机状态，如up、down
                #print('State : %s' % nm[host].state())
                # 遍历扫描协议，tcp、udp
                for proto in nm[host].all_protocols():
                    #print('--------------')
                    # 输出协议名
                    #print('Protocol : %s' % proto)
                    # 获取协议的所有扫描端口
                    lport = list(nm[host][proto].keys())
                    # 端口列表排序
                    lport.sort()
                    # 遍历端口输出端口与状态
                    for port in lport:
                        if nm[host][proto][port]['state'] != "open":
                            result_rows.append([host, port])
        return result_rows
    except Exception as e:
        print("Scan error:" + str(e))
def ip_list_scan():
    ips = input("the ip_list file?\n")
    ip, ip_ports = file_gen_ports(ips)
    scan_rows = my_scan(ip_ports)
    print(ip, scan_rows)
    return ip, scan_rows
