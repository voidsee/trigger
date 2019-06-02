#!/usr/bin/env python
# coding=utf-8
class Evaluate:
    def __init__(self, bound=(1,6,3), dnuob=(-1,-2), p=[1,1,1],\
             report=[["192.168.123.1","3306","http","phpinfo"],]):
        """score weighting(default 1,6,3), 
        minus score(default -1,-2), 
        probability(default 1,1,1)"""
        self.report = report
        self.score = [0,0,0]
        self.bound = bound
        self.bound_sum = sum(bound)
        self.dnuob = dnuob
        if p[0]>1:
            p[0]=1
        if p[1]>1:
            p[1]=1
        if p[2]>1:
            p[2]=1
        self.p = p

    def get_report(self, report):
        """get report from file"""
        self.report=[]
        try:
            with open(report, "r") as fd:
                line = fd.readline()
                while line:
                    self.report.append(line.split())
                    line = fd.readline()
                #self.report.append(fd.read().splitlines().split())
            if len(self.report[0])!=4:
                print("report format error,should be 4 colums\nip port server bug")
            else:
                self.split_report()
            return self.report
        except:
            print("report format error or report doesn't exist!")

    def get_table(self,table):
        """pull table """
        self.table = table

    def bad_points(self,table):
        """get bad table"""
        if len(table)==2:
            self.n_ips, self.n_ip_ports = table

    def split_report(self, ):
        """split report into three parts"""
        self.rpt =[[],[],[]]
        for i in self.report:
            if i[1]=='None':
                self.rpt[0].append(i[0])
            elif i[3]=='None':
                self.rpt[1].append([i[0],int(i[1])])
            else:
                self.rpt[2].append([i[0],int(i[1]),i[3]])
    

    def stat_ip(self,A=100):
        """statistics ip"""
        for ip in self.table[0]:
            if ip in self.rpt[0]:
                self.score[0] += 1
        self.score[0] = self.score[0]/len(self.table[0]) * self.bound[0]/self.bound_sum * A
    def stat_n_ip(self,):
        """statistics wrong ip"""
        for ip in self.n_ips:
            if ip in self.rpt[0]:
                self.score[0] -= abs(self.dnuob[0])

    def stat_port(self,A=100):
        """statistics port"""
        for ip_port in self.table[1]:
            if ip_port in self.rpt[1]:
                self.score[1] += 1
        self.score[1] = self.score[1]/len(self.table[1]) * self.bound[1]/self.bound_sum * A
    def stat_n_port(self,):
        """statistics wrong port"""
        for ip in self.n_ip_ports:
            if ip in self.rpt[0]:
                self.score[1] -= abs(self.dnuob[1])

    def stat_bug(self, num=0, A=100):
        """statistics loophole"""
        if num:
            self.score[2] = num
            if num>len(self.table[2]):
                self.score[2] = len(self.table[2])
        else:
            for bug in self.table[2]:
                for rpt_bug in self.rpt[2]:
                    if bug[:2]==rpt_bug[:2] \
                            and (bug[2] in rpt_bug[2] or rpt_bug[2] in bug[2]):
                        self.score[2] += 1
        self.score[2] = self.score[2]/len(self.table[2]) * self.bound[2]/self.bound_sum * A
    def corrector(self,A=100):
        """correct scores. eg:score/0.8"""
        self.score = list(map(lambda y,x:y/x, self.score, self.p))
        for i in range(3):
            if self.score[i]>self.bound[i]/self.bound_sum * A:
                self.score[i]=self.bound[i]/self.bound_sum * A
        self.stat_n_ip()
        self.stat_n_port()

    def stat(self,A=100):
        self.stat_ip(A=A)
        self.stat_port(A=A)
        self.stat_bug(A=A)
        self.corrector(A=A)
        return [self.score[0],self.score[1],self.score[2],sum(self.score)]



if __name__ == '__main__':
    from pprint import pprint

    eva = Evaluate([2,3,5], [-1,-2],[0.9,0.8,0.6])
    table=[["12.12.12.12"],[["12.12.12.12",12],],[["12.12.12.12",12,"bug"]]]
    eva.get_table(table)
    eva.bad_points([['127.0.0.1',],[['127.0.0.1',90],]])
    print("report");pprint(eva.get_report("report"))
    print("table");pprint(eva.table)
    print("split report");pprint(eva.rpt)
    eva.stat()
    
