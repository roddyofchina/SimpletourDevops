#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import time,os

from celery import Celery
from django.core.mail import send_mail
from Publicapi.saltstackapi.SaltConApi import SaltApi
from Publicapi.dockerapi.Manager import Dockerapi
from dockermanager.Docker_Controler import GetDockerServerinfo,GetDockerImages
from datetime import timedelta
from servermanager.models import *

from Publicapi.saltstackapi.Assets_Module import *

from django.conf import settings


from django.core import signals
from django.db import close_old_connections

# 取消信号关联，实现数据库长连接
signals.request_finished.disconnect(close_old_connections)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimpletourDevops.settings')

celery = Celery('tasks', backend='redis://192.168.2.232:6379/0',broker='redis://192.168.2.232:6379/0')



celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



celery.conf.update(
    CELERYBEAT_SCHEDULE = {
        'every-minute': {
            'task': 'webapp.tasks.DockerServers',
            'schedule': timedelta(seconds=10)
        },
    }
)


EMAIL_URL = 'http://192.168.4.223:8888/web/activate'
Reset_Pass = 'http://192.168.4.223:8888/web/resetpass'

@celery.task
def sendmail(mail):
    print "++++++++++++++++++++++++++++++++++"
    print('sending mail to %s ......' %mail['to'])
    time.sleep(5.0)
    print('mail sent.')
    emailmessages="用户注册激活邮件，请您点击: %s/%s" %(EMAIL_URL,mail['string'])
    send_mail(u"SimpletourDevops用户激活邮件",emailmessages,'923401910@qq.com',[mail['to'],],fail_silently=True)
    print "---------------------------------"
    return mail['to']


@celery.task
def resetpass(mail):
    print "++++++++++++++++++++++++++++++++++"
    print('sending mail to %s ......' %mail['to'])
    time.sleep(5.0)
    print('mail sent.')
    emailmessages="用户重置密码连接，请您点击:%s/%s" %(Reset_Pass,mail['string'])
    send_mail(u"SimpletourDevops重置密码",emailmessages,'923401910@qq.com',[mail['to'],],fail_silently=True)
    print "---------------------------------"
    return mail['to']

@celery.task()
def SaltGrains(minion):
    salt=SaltApi()
    print "------------------------"
    print "%s"  %minion['id']
    data=salt.grainsall(minion['id'])
    print "------------------------"
    return data


@celery.task()
def StopContainer(docker):
    print "-------------stop------container-----"
    dockerc=Dockerapi(docker['host'],docker['port'])
    data=dockerc.StopContainer(docker['container'])
    result={'resultInfo':u'容器停止成功!!', 'type': 'stop'}
    return {'result': result}

@celery.task()
def StartContainer(IP,port,container):
    print "|------------start------container------------|"
    dockerc=Dockerapi(IP,port)
    data = dockerc.StartContainer(container)
    result={'resultInfo':u'容器启动成功!!', 'type':'start'}
    return {'result': result}

@celery.task()
def RestartContainer(IP,port,container):
    print "-------------restart---container %s " % container
    dockerc=Dockerapi(IP,port)
    dockerc.RestartContainer(container)
    result={'resultInfo':u'重启容器成功!!','type':'restart'}
    print "ssssssssssssssssss"
    return {'result': result}

@celery.task()
def SaltGrainsAll():
    salt=SaltApi()
    print "----------Grainsall------------"
    clientkey=salt.List_all_keys()['minions']
    for i in clientkey:
        data=salt.grainsall(i)
    return clientkey

#定时任务
@celery.task()
def DockerServers():
    print u"-----------------获取docker容器列表及状态---------------"
    containerdata=GetDockerServerinfo()
    print u"-----------------获取成功-----------------------"
    print u"-----------------获取最新images列表-------------"
    imagedata=GetDockerImages()
    print u"-----------------获取镜像列表成功---------------"
    return containerdata,imagedata

#更新资产
@celery.task()
def UpdateServerInfo(serverid):
    salt = SaltApi()
    serverdata = Server.objects.get(id=serverid)
    saltid=serverdata.saltid
    data=salt.grainsall(saltid)
    ServerInfo=data

    #CPU信息
    CpuData=ServerCPUInfo(ServerInfo,saltid)
    CpuINFO=CpuData.ServerCPU()

    #DISK信息
    DiskData =ServerDiskInfo(ServerInfo,saltid)
    DiskINFO=DiskData.ServerDISK()

    #NIC信息
    NICData = ServerNICInfo(ServerInfo,saltid)
    NICINFO=NICData.ServerNIC()
    BaseINFO=CpuINFO['Serverbaseinfo']

    #--------------------------更新CPU信息-------------------------
    parentsn=CpuINFO['Serverbaseinfo']['sn']
    Cpudict=CpuINFO['servercpuinfo']
    Thread=Cpudict['thread']
    L1cache=Cpudict['L1cache']
    L2cache=Cpudict['L2cache']
    L3cache=Cpudict['L3cache']
    model=Cpudict['model']
    Vendordata=Cpudict['model']
    Vendor=Vendordata.split()[0]
    Architecture=Cpudict['architecture']
    cpu_mhz=Cpudict['cpu_mhz']
    uuid=Cpudict['uuid']

    if Cpu.objects.filter(parent_sn=parentsn):
        ChangeCpu=Cpu.objects.get(parent_sn=parentsn)
        ChangeCpu.Thread=Thread
        ChangeCpu.L1cache=L1cache
        ChangeCpu.L2cache=L2cache
        ChangeCpu.L3cache=L3cache
        ChangeCpu.Vendor=Vendor
        ChangeCpu.model=model
        ChangeCpu.Architecture = Architecture
        ChangeCpu.cpu_mhz=cpu_mhz
        ChangeCpu.parent_sn = parentsn
        ChangeCpu.uuid= uuid
        ChangeCpu.save()
    else:
        NewCpu=Cpu(Thread=Thread,
                   uuid=uuid,
                   model=model,
                   Architecture=Architecture,
                   cpu_mhz=cpu_mhz,
                   L1cache=L1cache,
                   Vendor=Vendor,
                   L2cache=L2cache,
                   L3cache=L3cache,
                   parent_sn=parentsn,)
        NewCpu.save()


    #--------------------------更新服务器信息------------------------
    serverdata.hostname = BaseINFO['hostname']
    serverdata.sn = BaseINFO['sn']
    if Cpu.objects.filter(parent_sn=BaseINFO['sn']):
        Cpuid=Cpu.objects.get(parent_sn=parentsn)
        serverdata.cpu = Cpuid

    serverdata.cpu_count = BaseINFO['cpu_count']
    serverdata.saltid = BaseINFO['saltid']
    serverdata.mem = BaseINFO['mem']
    serverdata.swap = BaseINFO['swap']
    serverdata.platform = BaseINFO['platform']
    serverdata.system = BaseINFO['system']
    serverdata.version = BaseINFO['version']
    serverdata.cpu_core_count =BaseINFO['cpu_core_count']
    serverdata.save()


    #---------------------------获取网卡信息----------------------------
    Nicdict=NICINFO['servernicinfo']['nicinfo']
    parentsn=NICINFO['Serverbaseinfo']['sn']
    for nicname,nicvalue in Nicdict.items():
        #排除lo和docker网卡
        if nicname not in ['eth1','eth0','em1','em0','p3p1','p1p1','p8p1']:
            continue
        if nicvalue.get('inet'):
            mac = nicvalue['hwaddr']
            Model = nicvalue['Model']
            nicstatus = nicvalue['up']
            uuid = nicvalue['uuid']
            name = nicname
            ip = nicvalue['inet'][0]['address']
            netmask = nicvalue['inet'][0]['netmask']

            if NIC.objects.filter(mac=mac):
                OldNic=NIC.objects.get(mac=mac)
                OldNic.uuid = uuid
                OldNic.name = name
                OldNic.model = Model
                OldNic.ip = ip
                OldNic.mac = mac
                OldNic.parent_sn = parentsn
                OldNic.netmask = netmask
                OldNic.nicstatus = nicstatus
                OldNic.save()
            else:
                Newnic=NIC(uuid=uuid,name=name,model=Model,parent_sn=parentsn,ip=ip,mac=mac,netmask=netmask,nicstatus=nicstatus)
                Newnic.save()
        else:
            continue

    #删除以前网卡信息
    for nic in serverdata.nic.all():
        serverdata.nic.remove(nic)

    #添加网卡到服务器
    nicdata = NIC.objects.filter(parent_sn=parentsn)
    for nic in nicdata:
        sdata = Server.objects.get(sn=parentsn)
        sdata.nic.add(nic)

    #---------------获取硬盘信息-------------------------
    parentsn=DiskINFO['Serverbaseinfo']['sn']
    Diskdict=DiskINFO['serverdiskinfo']['diskinfo']
    for diskname,diskvalue in Diskdict.items():
        name = diskvalue['name']
        uuid = diskvalue['uuid']
        capacity= diskvalue['size']
        disk_type=diskvalue['type']

        if Disk.objects.filter(uuid=uuid):
            for OldDisk in Disk.objects.filter(parent_sn=parentsn):
                OldDisk.name = name
                OldDisk.capacity=capacity
                OldDisk.parent_sn=parentsn
                OldDisk.disk_type = disk_type
                OldDisk.save()
        else:
            NewDisk=Disk(name=name,uuid=uuid,parent_sn=parentsn,capacity=capacity,disk_type=disk_type)
            NewDisk.save()

    #删除以前磁盘信息
    for disk in serverdata.disk.all():
        serverdata.disk.remove(disk)

    #添加磁盘到服务器
    diskdata = Disk.objects.filter(parent_sn=parentsn)
    for disk in diskdata:
        sdata = Server.objects.get(sn=parentsn)
        sdata.disk.add(disk)

    serverinfo={}
    Info_Data = Server.objects.get(id=serverid)
    serverinfo['hostname']=Info_Data.hostname
    serverinfo['last_update']= Info_Data.update_time.strftime("%Y-%m-%d %H:%M:%S")
    serverinfo['sn'] = Info_Data.sn
    serverinfo['cpu'] = Info_Data.cpu_count
    niclist=[]
    for i in Info_Data.nic.all():
        niclist.append(i.ip)
    serverinfo['nic'] = niclist

    disklist=[]
    for d in Info_Data.disk.all():
        disklist.append(d.name)
    serverinfo['disk']=disklist

    return {'result': serverinfo}


@celery.task()
def DeleteContainer(IP,port,container):
    print "-------------delete---container %s " %container
    dockerc=Dockerapi(IP,port)
    dockerc.removeContainer(container,v=False,force=True)
    result={'resultInfo':u'容器删除成功!!','type':'delete'}
    return {'result': result}








