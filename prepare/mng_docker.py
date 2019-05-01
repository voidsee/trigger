#!/usr/bin/python3
import docker
from split import gather_ports,split_ports
client = docker.from_env()

dks = { 'nginx':{'ports':{'80/tcp':3333}, 'environment':None},
        'httpd':{'ports':{'80/tcp':3399}, 'environment':None},
        'mysql':{'ports':{'3306/tcp':3388}, 'environment':["MYSQL_ROOT_PASSWORD=123456"]}}


def run_ctnrs(ip_ports):
    """run(image, command=None, **kwargs)"""
    ip_port_srv=[]; i=0
    splited_ports = split_ports(ip_ports, len(dks))

    for img in dks:
        for _ in dks[img]['ports']:
            dks[img]['ports'][_]=gather_ports(splited_ports[i])
        try:
            client.containers.run(img_latest(img), detach=True,\
                    ports=dks[img]['ports'],\
                    environment=dks[img]['environment'])
        except Exception as e:
            print(str(e))

        for j in range(len(splited_ports[i])):
            splited_ports[i][j].append(str(img))
        ip_port_srv.extend(splited_ports[i])
        i+=1
    return ip_port_srv

def stp_ctnrs():
    for ctnr in client.containers.list():
        ctnr.stop()

def get_id(dk_list):
    return [dk.short_id for dk in dk_list]
def img_latest(img):
    return img+':latest' if not ':' in img else img


if __name__ == '__main__':
    from pprint import pprint
    ip_ports = [['172.17.0.1', 1584],
                 ['220.181.112.244', 1530],
                 ['202.89.233.101', 1307],
                 ['220.181.112.244', 1749],
                 ['172.17.0.1', 1506],
                 ['202.89.233.101', 1700]]
    pprint(ip_ports)
    a = run_ctnrs(ip_ports)
    pprint(a)
    #stp_ctnrs()

