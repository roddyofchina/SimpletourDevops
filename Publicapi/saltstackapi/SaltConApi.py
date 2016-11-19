#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'
import urllib,urllib2
import json
from Assets_Module import ServerBaseInfo,ServerCPUInfo,ServerNICInfo,ServerDiskInfo


class SaltApi(object):

    __token = ''
    print __token
    def __init__(self):
        self.__url = 'http://192.168.2.150:8000'
        self.__user= 'roddy'
        self.__pass = 'roudy_123456'
        params = {'eauth': 'pam','username':self.__user,'password': self.__pass}

        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.PostRequest(obj, parurl='/login')
        try:
            self.__token = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def PostRequest(self,obj,parurl='/'):
        url = self.__url + parurl
        headers = {'X-Auth-Token'   : self.__token}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def grains(self,tgt,args):
        params={'client':'local','tgt': tgt, 'fun': 'grains.item','arg': args}
        obj=urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]
        return ret

    def grainsall(self,tgt):
        params={'client':'local','tgt': tgt, 'fun': 'grains.items'}
        obj=urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]
        return ret

    def List_all_keys(self):
        params={'client':'wheel', 'fun':'key.list_all'}
        obj=urllib.urlencode(params)
        content=self.PostRequest(obj)
        ret = content['return'][0]['data']['return']
        return ret


if __name__ == '__main__':
    salt=SaltApi()
    data=salt.grainsall(u'192.168.2.147')
    server=ServerDiskInfo(data, u'192.168.2.147')
    server=ServerCPUInfo(data,u'192.168.2.147')
    print server.ServerCPU()

#    print salt.grains('server.192.168.2.70','zmqversion')
#    clientkey=salt.List_all_keys()['minions']
#    Servers={}
#    for i in clientkey:
#        data=salt.grainsall(i)
#        server=ServerNICInfo(data,i)
#        serverinfo=server.ServerNIC()
#        print serverinfo






