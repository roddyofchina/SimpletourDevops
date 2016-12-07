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



if __name__ == '__main__':
    GetMinionConf()

