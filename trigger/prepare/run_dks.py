#!/usr/bin/python3
import docker
from random import random, sample
from split import Ip_op

class Dkr:
    def __init__(self, ip_ports=[['127.0.0.1', 80],]):
        self.client = docker.from_env()
        self.ip_ports = ip_ports
        self.imgs = { 'httpd':{'ports':{'80/tcp':7080}, 'environment':None},
                      'mysql':{'ports':{'3306/tcp':3307}, 'environment':["MYSQL_ROOT_PASSWORD=123456"]},}
        self.info = { 'httpd':': phpinfo bug',
                      'mysql':': empty password',}

    def run_ctnrs(self,):
        """run(image, command=None, **kwargs)"""
        ip_port_srv=[]; i=0
        ip_op = Ip_op()
        splited_ports = ip_op.split_ports(self.ip_ports, len(self.imgs))

        for img in self.imgs:
            for _ in self.imgs[img]['ports']:
                self.imgs[img]['ports'][_]=ip_op.gather_ports(splited_ports[i])
            try:
                self.client.containers.run(self.img_latest(img), detach=True,\
                        ports=self.imgs[img]['ports'],\
                        environment=self.imgs[img]['environment'])
            except Exception as e:
                print(str(e))

            for j in range(len(splited_ports[i])):
                splited_ports[i][j].append(str(img)+self.info[img])
            ip_port_srv.extend(splited_ports[i])
            i+=1
        return ip_port_srv
    def img_latest(self, img):
        """ 'img' -> 'img:latest' """
        return img+':latest' if not ':' in img else img

    def stp_ctnrs(self,):
        """stop all running containers"""
        for ctnr in client.containers.list():
            ctnr.stop()

    def get_id(self, dk_list):
        """get docker id from docker list"""
        return [dk.short_id for dk in dk_list]


if __name__ == '__main__':
    from pprint import pprint
    ip_ports = [['172.17.0.1', 1584],
                 ['220.181.112.244', 1530],
                 ['202.89.233.101', 1307],
                 ['220.181.112.244', 1749],
                 ['172.17.0.1', 1506],
                 ['202.89.233.101', 1700]]
    pprint(ip_ports)
    dkr = Dkr(ip_ports)
    a = dkr.run_ctnrs()
    pprint(a)
    #stp_ctnrs()

