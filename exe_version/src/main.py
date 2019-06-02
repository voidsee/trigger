from get_ready import get_ready
from assess import assess
from deploy import deploy
from os import system

######################################################
def welcome():
    help_meta()
    print("For help, type '?', '\q' for quit.")
######################################################
def start_fun():
    ip_file = input("input ip file name:")
    try:
        get_ready(ip_file)
    except:
        print("something wrong when loading ip file!")

def deploy_fun():
    iface  = input("input interface name [eth0]:")
    try:
        if not len(iface):
            iface = "eth0"
        deploy(iface)
    except:
        print("Abort!")

def assess_fun():
    ip_file = input("input ip file name:")
    report = input("input report file name:")
    try:
        print("assessing...")
        assess(report, ip_file)
    except:
        print("something wrong when loading file!")


command = {'start':start_fun,
        'deploy':deploy_fun,
        'assess':assess_fun,}
######################################################
def help_meta():
    try:
        with open("README","r") as man:
            content = man.read()
            print(content)
    except:
        print("help file lost!")
def ls_meta():
    for k in command:
        print(k,end='\t')
    print()
def clear_meta():system("clear")

######################################################

def main():
    welcome()
    while True:
        f = input("trigger>");print('\b',end='')
        if f=='?': help_meta()
        elif f=='ls': ls_meta()
        elif f=='cls': clear_meta()
        elif f=='\q': return 0
        elif f in command: command[f]()
        else: print("command error!")

main()
