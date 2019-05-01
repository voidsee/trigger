from nmap_t2 import *
from gen_ip_ports import *

file_name = input("input file name:")
n = int(input("input number"))
ips_ports = gen_ports(get_ip_list(file_name), n)

print(ips_ports)
