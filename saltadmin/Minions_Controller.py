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
        errors_count = []

        for task,taskresult in resultdata.items():

            taskLinedict ={}
            taskLinedict['ID'] = task.split('|')[1].strip('_').lstrip('-')
            taskLinedict['Name'] = task.split('|')[2].strip('_').lstrip('-')
            if taskresult['result']  == False:
                errors_count.append(taskresult)
            taskLinedict['Result'] =taskresult['result']
            taskLinedict['Comment'] = taskresult['comment']
            if  not taskresult.has_key('start_time'):
                taskresult['Started'] = ''
            else:
                taskresult['Started'] = taskresult['start_time']
            if not taskresult.has_key('duration'):
                taskresult['Duration'] = ''
            else:
                taskresult['Duration'] = taskresult['duration']
            taskLinedict['Changes'] = taskresult['changes']
            list.append(taskLinedict)

        result_dict_list = {'url':resultkey,'result': list,'error':len(errors_count),'success':len(list) - len(errors_count)}
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
    #a={u'192.168.2.148': {u'user_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'User zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.381761', u'result': None, u'duration': 16.003, u'__run_num__': 1, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-start-file_|-/etc/rc.local_|-append': {u'comment': u'File /etc/rc.local is set to be updated', u'pchanges': {}, u'name': u'/etc/rc.local', u'start_time': u'10:41:43.439903', u'result': None, u'duration': 1.483, u'__run_num__': 7, u'changes': {u'diff': u'--- \n\n+++ \n\n@@ -13,3 +13,4 @@\n\n touch /var/lock/subsys/local\n mount  /home/data /data  --bind\n mount /data/docker /var/lib/docker --bind\n+/etc/init.d/zabbix_agentd start'}, u'__id__': u'start-file'}, u'file_|-zabbix-client-transport_|-/usr/local/src/zabbix-3.0.5-client.tar.gz_|-managed': {u'comment': u'The file /usr/local/src/zabbix-3.0.5-client.tar.gz is set to be changed', u'pchanges': {u'newfile': u'/usr/local/src/zabbix-3.0.5-client.tar.gz'}, u'name': u'/usr/local/src/zabbix-3.0.5-client.tar.gz', u'start_time': u'10:41:43.399380', u'result': None, u'duration': 9.981, u'__run_num__': 2, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'cmd_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd start_|-run': {u'comment': u'Command "/etc/init.d/zabbix_agentd start" would have been executed', u'name': u'/etc/init.d/zabbix_agentd start', u'start_time': u'10:41:43.439464', u'result': None, u'duration': 0.355, u'__run_num__': 6, u'changes': {}, u'__id__': u'zabbix-start-sh'}, u'group_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'Group zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.380688', u'result': None, u'duration': 0.683, u'__run_num__': 0, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-zabbix-file-copy_|-/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf_|-managed': {u'comment': u'The file /usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf'}, u'name': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf', u'start_time': u'10:41:43.410485', u'result': None, u'duration': 24.638, u'__run_num__': 4, u'changes': {}, u'__id__': u'zabbix-file-copy'}, u'cmd_|-zabbix-client-transport_|-cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/_|-run': {u'comment': u'Command "cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/" would have been executed', u'name': u'cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/', u'start_time': u'10:41:43.410143', u'result': None, u'duration': 0.276, u'__run_num__': 3, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'file_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd_|-managed': {u'comment': u'The file /etc/init.d/zabbix_agentd is set to be changed', u'pchanges': {u'newfile': u'/etc/init.d/zabbix_agentd'}, u'name': u'/etc/init.d/zabbix_agentd', u'start_time': u'10:41:43.435245', u'result': None, u'duration': 3.886, u'__run_num__': 5, u'changes': {}, u'__id__': u'zabbix-start-sh'}}, u'192.168.2.147': {u'user_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'User zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.649409', u'result': None, u'duration': 16.626, u'__run_num__': 1, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-start-file_|-/etc/rc.local_|-append': {u'comment': u'File /etc/rc.local is set to be updated', u'pchanges': {}, u'name': u'/etc/rc.local', u'start_time': u'10:41:43.759598', u'result': None, u'duration': 2.015, u'__run_num__': 7, u'changes': {u'diff': u'--- \n\n+++ \n\n@@ -13,3 +13,4 @@\n\n touch /var/lock/subsys/local\n mount  /home/data /data  --bind\n mount /data/docker /var/lib/docker --bind\n+/etc/init.d/zabbix_agentd start'}, u'__id__': u'start-file'}, u'file_|-zabbix-client-transport_|-/usr/local/src/zabbix-3.0.5-client.tar.gz_|-managed': {u'comment': u'The file /usr/local/src/zabbix-3.0.5-client.tar.gz is set to be changed', u'pchanges': {u'newfile': u'/usr/local/src/zabbix-3.0.5-client.tar.gz'}, u'name': u'/usr/local/src/zabbix-3.0.5-client.tar.gz', u'start_time': u'10:41:43.667990', u'result': None, u'duration': 20.692, u'__run_num__': 2, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'cmd_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd start_|-run': {u'comment': u'Command "/etc/init.d/zabbix_agentd start" would have been executed', u'name': u'/etc/init.d/zabbix_agentd start', u'start_time': u'10:41:43.758629', u'result': None, u'duration': 0.728, u'__run_num__': 6, u'changes': {}, u'__id__': u'zabbix-start-sh'}, u'group_|-zabbix-user-group_|-zabbix_|-present': {u'comment': u'Group zabbix set to be added', u'name': u'zabbix', u'start_time': u'10:41:43.647126', u'result': None, u'duration': 1.619, u'__run_num__': 0, u'changes': {}, u'__id__': u'zabbix-user-group'}, u'file_|-zabbix-file-copy_|-/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf_|-managed': {u'comment': u'The file /usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf'}, u'name': u'/usr/local/zabbix-3.0.5/etc/zabbix_agentd.conf', u'start_time': u'10:41:43.690624', u'result': None, u'duration': 56.148, u'__run_num__': 4, u'changes': {}, u'__id__': u'zabbix-file-copy'}, u'cmd_|-zabbix-client-transport_|-cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/_|-run': {u'comment': u'Command "cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/" would have been executed', u'name': u'cd /usr/local/src/ && tar -zxf zabbix-3.0.5-client.tar.gz -C /usr/local/', u'start_time': u'10:41:43.689750', u'result': None, u'duration': 0.66, u'__run_num__': 3, u'changes': {}, u'__id__': u'zabbix-client-transport'}, u'file_|-zabbix-start-sh_|-/etc/init.d/zabbix_agentd_|-managed': {u'comment': u'The file /etc/init.d/zabbix_agentd is set to be changed', u'pchanges': {u'newfile': u'/etc/init.d/zabbix_agentd'}, u'name': u'/etc/init.d/zabbix_agentd', u'start_time': u'10:41:43.746988', u'result': None, u'duration': 11.198, u'__run_num__': 5, u'changes': {}, u'__id__': u'zabbix-start-sh'}}}
    a={u'192.168.2.147': {u'file_|-nginx-config_|-/usr/local/nginx/conf/nginx.conf_|-managed': {u'comment': u'The file /usr/local/nginx/conf/nginx.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/nginx/conf/nginx.conf'}, u'retcode': 2, u'start_time': u'12:00:11.704011', u'__id__': u'nginx-config', u'result': None, u'duration': 62.022, u'__run_num__': 6, u'changes': {}, u'name': u'/usr/local/nginx/conf/nginx.conf'}, u'file_|-/usr/local/nginx/conf/vhosts/_|-/usr/local/nginx/conf/vhosts/_|-directory': {u'comment': u'The following files will be changed:\n/usr/local/nginx/conf/vhosts: directory - new\n', u'pchanges': {u'/usr/local/nginx/conf/vhosts': {u'directory': u'new'}}, u'retcode': 2, u'start_time': u'12:00:11.766317', u'__id__': u'/usr/local/nginx/conf/vhosts/', u'result': None, u'duration': 0.813, u'__run_num__': 7, u'changes': {}, u'name': u'/usr/local/nginx/conf/vhosts/'}, u'file_|-nginx-install_|-/usr/local/src/nginx-1.2.0.tar.gz_|-managed': {u'comment': u'Source file salt://nginx/files/nginx-1.2.0.tar.gz not found', u'_stamp': u'2016-12-15T12:02:16.749601', u'pchanges': [False, u'Source file salt://nginx/files/nginx-1.2.0.tar.gz not found'], u'return': u'Error: file.managed', u'retcode': 2, u'success': False, u'start_time': u'12:00:11.690524', u'jid': u'20161215200215675300', u'duration': 12.813, u'result': False, u'__id__': u'nginx-install', u'fun': u'state.sls', u'__run_num__': 4, u'changes': {}, u'id': u'192.168.2.147', u'name': u'/usr/local/src/nginx-1.2.0.tar.gz'}, u'user_|-www-user-group_|-www_|-present': {u'comment': u'User www set to be added', u'retcode': 2, u'start_time': u'12:00:11.674525', u'__id__': u'www-user-group', u'result': None, u'duration': 15.774, u'__run_num__': 3, u'changes': {}, u'name': u'www'}, u'file_|-pcre-install_|-/usr/local/src/pcre-8.37.tar.gz_|-managed': {u'comment': u'The file /usr/local/src/pcre-8.37.tar.gz is set to be changed', u'pchanges': {u'newfile': u'/usr/local/src/pcre-8.37.tar.gz'}, u'retcode': 2, u'start_time': u'12:00:11.641509', u'__id__': u'pcre-install', u'result': None, u'duration': 22.872, u'__run_num__': 0, u'changes': {}, u'name': u'/usr/local/src/pcre-8.37.tar.gz'}, u'file_|-/usr/local/nginx/conf/vhosts/www.test.com.conf_|-/usr/local/nginx/conf/vhosts/www.test.com.conf_|-managed': {u'comment': u'The file /usr/local/nginx/conf/vhosts/www.test.com.conf is set to be changed', u'pchanges': {u'newfile': u'/usr/local/nginx/conf/vhosts/www.test.com.conf'}, u'retcode': 2, u'start_time': u'12:00:11.767427', u'__id__': u'/usr/local/nginx/conf/vhosts/www.test.com.conf', u'result': None, u'duration': 431.954, u'__run_num__': 8, u'changes': {}, u'name': u'/usr/local/nginx/conf/vhosts/www.test.com.conf'}, u'cmd_|-nginx-install_|-cd /usr/local/src/ && tar zxf nginx-1.8.0.tar.gz && cd nginx-1.8.0 && ./configure --prefix=/usr/local/nginx --user=www --group=www --with-http_ssl_module --with-http_stub_status_module --with-file-aio --with-http_dav_module --with-pcre=/usr/local/src/pcre-8.37 && make && make install && chown -R www. /usr/local/nginx_|-run': {u'comment': u'One or more requisite failed: nginx.install.nginx-install', u'__run_num__': 5, u'__sls__': u'nginx.install', u'changes': {}, u'result': False}, u'file_|-nginx-service_|-/usr/lib/systemd/system/nginx.service_|-managed': {u'comment': u'The file /usr/lib/systemd/system/nginx.service is set to be changed', u'pchanges': {u'newfile': u'/usr/lib/systemd/system/nginx.service'}, u'retcode': 2, u'start_time': u'12:00:12.199726', u'__id__': u'nginx-service', u'result': None, u'duration': 13.078, u'__run_num__': 9, u'changes': {}, u'name': u'/usr/lib/systemd/system/nginx.service'}, u'file_|-log_logrotate_|-/etc/logrotate.d/logrotate_nginx_|-managed': {u'comment': u'The file /etc/logrotate.d/logrotate_nginx is set to be changed', u'pchanges': {u'newfile': u'/etc/logrotate.d/logrotate_nginx'}, u'retcode': 2, u'start_time': u'12:00:12.229231', u'__id__': u'log_logrotate', u'result': None, u'duration': 13.148, u'__run_num__': 11, u'changes': {}, u'name': u'/etc/logrotate.d/logrotate_nginx'}, u'cmd_|-pcre-install_|-cd /usr/local/src/ && tar zxf pcre-8.37.tar.gz && cd pcre-8.37 && ./configure --prefix=/usr/local/pcre  && make && make install_|-run': {u'comment': u'Command "cd /usr/local/src/ && tar zxf pcre-8.37.tar.gz && cd pcre-8.37 && ./configure --prefix=/usr/local/pcre  && make && make install" would have been executed', u'retcode': 2, u'start_time': u'12:00:11.665282', u'__id__': u'pcre-install', u'result': None, u'duration': 6.168, u'__run_num__': 1, u'changes': {}, u'name': u'cd /usr/local/src/ && tar zxf pcre-8.37.tar.gz && cd pcre-8.37 && ./configure --prefix=/usr/local/pcre  && make && make install'}, u'cmd_|-nginx-service_|-chmod +x /usr/lib/systemd/system/nginx.service && systemctl enable nginx.service && systemctl start nginx.service_|-run': {u'comment': u'Command "chmod +x /usr/lib/systemd/system/nginx.service && systemctl enable nginx.service && systemctl start nginx.service" would have been executed', u'retcode': 2, u'start_time': u'12:00:12.213134', u'__id__': u'nginx-service', u'result': None, u'duration': 15.835, u'__run_num__': 10, u'changes': {}, u'name': u'chmod +x /usr/lib/systemd/system/nginx.service && systemctl enable nginx.service && systemctl start nginx.service'}, u'group_|-www-user-group_|-www_|-present': {u'comment': u'Group www set to be added', u'name': u'www', u'start_time': u'12:00:11.672088', u'result': None, u'duration': 1.803, u'__run_num__': 2, u'changes': {}, u'__id__': u'www-user-group'}}}
    JobResultFromat(a)

