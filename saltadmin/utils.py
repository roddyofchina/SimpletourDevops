#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'
import commands
import os

def get_system_info():
    cmd_get_cpu_sockect=r"lscpu|grep Socket|awk '{print $NF}'"
    cmd_get_cpu_cores=r"cat /proc/cpuinfo|grep processor|wc -l"
    cmd_get_mem_total=r"free -m |head -n 2|tail -n 1|awk '{print $2}'"
    cmd_get_mem_used=r"free -m |tail -n 2|head -n 1|awk '{print $3}'"
    cmd_get_users_num=r"w -h |wc -l"
    cmd_get_uptime=r"uptime |awk -F',' '{print $1}'"
    cpu_sockets=commands.getoutput(cmd_get_cpu_sockect)
    res=os.system('lscpu &>/dev/null')
    if res != 0:
        cpu_sockets=1  #如果没有lscpu命令，默认的CPU个数为1个
    cpu_cores=commands.getoutput(cmd_get_cpu_cores)
    mem_total=commands.getoutput(cmd_get_mem_total)
    mem_used=commands.getoutput(cmd_get_mem_used)
    users=commands.getoutput(cmd_get_users_num)
    uptime=commands.getoutput(cmd_get_uptime)
    mem_percentage=round(float(mem_used)/float(mem_total)*100,2)
    mem_left_percentage=100-mem_percentage
    info_dict={'cpu_sockets':cpu_sockets,
               'cpu_cores':cpu_cores,
               'mem_total':mem_total,
               'mem_used':mem_used,
               'mem_percentage':mem_percentage,
               'users':users,
               'uptime':uptime,
               'mem_left_percentage':mem_left_percentage}

    return info_dict