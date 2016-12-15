#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimpletourDevops.settings")
import django
django.setup()
import datetime
from saltadmin.models import *
from Publicapi.saltstackapi.SaltConApi import SaltApi
import threading
import json


def GetALLkeys():
    saltmaster = SaltServer.objects.all()

    for server in saltmaster:
        salt=SaltApi(server.url,server.username,server.password)
        minions,minions_pre,minions_rej,minions_deny =salt.List_all_keys()
        for i in minions:
            try:
                Minions.objects.create(minion=i, saltserver=server, status="Accepted")
            except:
                minion = Minions.objects.get(minion=i)
                minion.status = 'Accepted'
                minion.save()
        for pre in minions_pre:
            try:
                Minions.objects.create(minion=pre, saltserver=server, status="Unaccepted")
            except:
                minion = Minions.objects.get(minion=pre)
                minion.status = 'Unaccepted'
                minion.save()


        for rej in minions_rej:
            try:
                Minions.objects.create(minion=rej, saltserver=server, status="Rejected")
            except:
                minion = Minions.objects.get(minion=rej)
                minion.status = 'Rejected'
                minion.save()


        for deny in minions_deny:
            try:
                Minions.objects.create(minion=deny, saltserver=server, status="Denied")
            except:
                minion = Minions.objects.get(minion=deny)
                minion.status = 'Denied'
                minion.save()


def UpdateMinionInfo(mininboj,minions,url,username,password):
    salt = SaltApi(url, username, password)
    alive_minions = salt.Saltalive(minions)

    print alive_minions
    if minions in alive_minions:
        minion_status = True
    else:
        minion_status = False

    try:
        MinionStatus.objects.create(minion=mininboj, minion_status=minion_status)
    except:
        saltminion = MinionStatus.objects.get(minion=mininboj)
        alive_old = MinionStatus.objects.get(minion=mininboj).minion_status

        if minion_status != alive_old:
            saltminion.alive_time_last = datetime.datetime.now()
            saltminion.minion_status = minion_status
        print "-------------------------------%s" %(minion_status,)
        saltminion.alive_time_now = datetime.datetime.now()
        saltminion.save()


def GetMinionConf():
    GetALLkeys()
    MinionsData=Minions.objects.filter(status='Accepted')
    for minion in MinionsData:
        t=threading.Thread(target=UpdateMinionInfo,args=(minion,
                                                         minion.minion,
                                                         minion.saltserver.url,
                                                         minion.saltserver.username,
                                                         minion.saltserver.password))
        t.start()

    return "GET minion conf is Ok!!"



def GetJobs(url,username,password):
    salt = SaltApi(url,username,password)

    data = salt.runner("jobs.list_jobs")

    for j,info in data.items():
        if SaltJobs.objects.filter(jid=j):
            pass
        else:
            SaltJobs.objects.create(jid=j,args=info['Arguments'],function=info['Function'],
                                    startTime=info['StartTime'],target=info['Target'],user=info['User'],saltserver=url)


def GetSaltJobs():
    SaltMaster_data = SaltServer.objects.all()
    for salt in SaltMaster_data:
        t = threading.Thread(target=GetJobs,args=(salt.url,salt.username,salt.password))
        t.start()



def JobResultFromat(data):
    result=[]
    for resultkey,resultdata in data.items():
        list = []
        for task,taskresult in resultdata.items():
            taskLinedict ={}
            taskLinedict['ID'] = taskresult['__id__']
            taskLinedict['Name'] = taskresult['name']
            taskLinedict['Result'] =taskresult['result']
            taskLinedict['Comment'] = taskresult['comment']
            taskresult['Started'] = taskresult['start_time']
            taskresult['Duration'] = taskresult['duration']
            taskLinedict['Changes'] = taskresult['changes']
            list.append(taskLinedict)

        result_dict_list = {'url':resultkey,'result': list}
        result.append(result_dict_list)

    # for formatkey,formatresult in result.items():
    #     print formatkey
    #     for line in  formatresult:
    #         print "---------------------------------"
    #         for k,v in line.items():
    #             if isinstance(v,dict):
    #                 if len(v) == 0:
    #                     v = None
    #             print k+":",v
    #
    #     #result[k] = v

    return result





if __name__ == '__main__':
    #GetMinionConf()
    #GetSaltJobs()
    a={u'192.168.2.148': {u'user_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'User zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.381761', u'result': None, u'duration': 16.003, u'__run_num__': 1, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-start-file_|-/etc/rc.local_|-append': {u'comment': u'File /etc/rc.local is set to be updated', u'pchanges': {}, u'name': u'/etc/rc.local', u'start_time': u'10:41:43.439903', u'result': None, u'duration': 1.483, u'__run_num__': 7, u'changes': {u'diff': u'--- \n\n+++ \n\n@@ -13,3 +13,4 @@\n\n touch /var/lock/subsys/local\n mount  /home/data /data  --bind\n mount /data/docker /var/lib/docker --bind\n+/etc/init.d/zabbix_agentd start'}, u'__id__': u'start-file'}, u'file_|-zabbix-client-transport_|-/usr/local/src/zabbix-3.0.5-client.tar.gz_|-managed': {u'comment': u'The file /usr/local/src/zabbix-3.0.5-client.tar.gz is set to be changed', u'pchanges': {u'newfile': u'/usr/local/src/zabbix-3.0.5-client.tar.gz'}, u'name': u'/usr/local/src/zabbix-3.0.5-client.tar.gz', u'start_time': u'10:41:43.399380', u'result': None, u'duration': 9.981, u'__run_num__': 2, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'cmd_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd start_|-run': {u'comment': u'Command "/etc/init.d/zabbix_agentd start" would have been executed', u'name': u'/etc/init.d/zabbix_agentd start', u'start_time': u'10:41:43.439464', u'result': None, u'duration': 0.355, u'__run_num__': 6, u'changes': {}, u'__id__': u'zabbix-start-sh'}, u'group_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'Group zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.380688', u'result': None, u'duration': 0.683, u'__run_num__': 0, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-zabbix-file-copy_|-/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf_|-managed': {u'comment': u'The file /usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf'}, u'name': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf', u'start_time': u'10:41:43.410485', u'result': None, u'duration': 24.638, u'__run_num__': 4, u'changes': {}, u'__id__': u'zabbix-file-copy'}, u'cmd_|-zabbix-client-transport_|-cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/_|-run': {u'comment': u'Command "cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/" would have been executed', u'name': u'cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/', u'start_time': u'10:41:43.410143', u'result': None, u'duration': 0.276, u'__run_num__': 3, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'file_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd_|-managed': {u'comment': u'The file /etc/init.d/zabbix_agentd is set to be changed', u'pchanges': {u'newfile': u'/etc/init.d/zabbix_agentd'}, u'name': u'/etc/init.d/zabbix_agentd', u'start_time': u'10:41:43.435245', u'result': None, u'duration': 3.886, u'__run_num__': 5, u'changes': {}, u'__id__': u'zabbix-start-sh'}}, u'192.168.2.147': {u'user_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'User zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.649409', u'result': None, u'duration': 16.626, u'__run_num__': 1, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-start-file_|-/etc/rc.local_|-append': {u'comment': u'File /etc/rc.local is set to be updated', u'pchanges': {}, u'name': u'/etc/rc.local', u'start_time': u'10:41:43.759598', u'result': None, u'duration': 2.015, u'__run_num__': 7, u'changes': {u'diff': u'--- \n\n+++ \n\n@@ -13,3 +13,4 @@\n\n touch /var/lock/subsys/local\n mount  /home/data /data  --bind\n mount /data/docker /var/lib/docker --bind\n+/etc/init.d/zabbix_agentd start'}, u'__id__': u'start-file'}, u'file_|-zabbix-client-transport_|-/usr/local/src/zabbix-3.0.5-client.tar.gz_|-managed': {u'comment': u'The file /usr/local/src/zabbix-3.0.5-client.tar.gz is set to be changed', u'pchanges': {u'newfile': u'/usr/local/src/zabbix-3.0.5-client.tar.gz'}, u'name': u'/usr/local/src/zabbix-3.0.5-client.tar.gz', u'start_time': u'10:41:43.667990', u'result': None, u'duration': 20.692, u'__run_num__': 2, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'cmd_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd start_|-run': {u'comment': u'Command "/etc/init.d/zabbix_agentd start" would have been executed', u'name': u'/etc/init.d/zabbix_agentd start', u'start_time': u'10:41:43.758629', u'result': None, u'duration': 0.728, u'__run_num__': 6, u'changes': {}, u'__id__': u'zabbix-start-sh'}, u'group_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'Group zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.647126', u'result': None, u'duration': 1.619, u'__run_num__': 0, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-zabbix-file-copy_|-/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf_|-managed': {u'comment': u'The file /usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf'}, u'name': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf', u'start_time': u'10:41:43.690624', u'result': None, u'duration': 56.148, u'__run_num__': 4, u'changes': {}, u'__id__': u'zabbix-file-copy'}, u'cmd_|-zabbix-client-transport_|-cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/_|-run': {u'comment': u'Command "cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/" would have been executed', u'name': u'cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/', u'start_time': u'10:41:43.689750', u'result': None, u'duration': 0.66, u'__run_num__': 3, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'file_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd_|-managed': {u'comment': u'The file /etc/init.d/zabbix_agentd is set to be changed', u'pchanges': {u'newfile': u'/etc/init.d/zabbix_agentd'}, u'name': u'/etc/init.d/zabbix_agentd', u'start_time': u'10:41:43.746988', u'result': None, u'duration': 11.198, u'__run_num__': 5, u'changes': {}, u'__id__': u'zabbix-start-sh'}}}
    JobResultFromat(a)

