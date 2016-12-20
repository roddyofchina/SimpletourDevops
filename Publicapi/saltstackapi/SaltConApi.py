#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'
import urllib,urllib2
import json
import requests
import yaml
from Assets_Module import ServerBaseInfo,ServerCPUInfo,ServerNICInfo,ServerDiskInfo


class SaltApi(object):
    __token = ''
    def __init__(self,url,user,password):

        self.__url = url.rstrip('/')
        self.__user= user
        self.__pass = password
        params = {'eauth': 'pam','username':self.__user,'password': self.__pass}
        req = requests.post(url+'/login', data=params,allow_redirects=False)
        try:
            self.__token = req.headers['x-auth-token']
        except KeyError:
            raise KeyError

    def PostRequest(self,obj,parurl='/'):
        url = self.__url + parurl
        headers = {'X-Auth-Token': self.__token,'Accept': 'application/json'}
        req = requests.post(url, data=obj, headers=headers,verify=False)
        content = req.json()
        return content


    def grains(self,tgt,args):
        params={'client':'local','tgt': tgt, 'fun': 'grains.item','arg': args}
        content = self.PostRequest(params)
        ret = content['return'][0]
        return ret

    def grainsall(self,tgt):
        params={'client':'local','tgt': tgt, 'fun': 'grains.items'}
        content = self.PostRequest(params)
        ret = content['return'][0]
        return ret

    def pillarall(self,tgt):
        params = {'client': 'local', 'tgt': tgt, 'fun': 'pillar.items'}
        content = self.PostRequest(params)
        ret = content['return'][0]
        return ret


    def List_all_keys(self):
        params={'client':'wheel', 'fun':'key.list_all'}
        content=self.PostRequest(params)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        minions_deny = content['return'][0]['data']['return']['minions_denied']
        return minions, minions_pre, minions_rej, minions_deny


    def shell_remote_execution(self,tgt,arg):
        ''' Shell command execution with parameters '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': 'list'}
        content = self.PostRequest(params)
        jid = content['return'][0]['jid']
        return jid


    def Softwarete_deploy(self,tgt,arg):
        '''执行salt.sls 远程部署程序'''

        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls','arg':arg, 'expr_form': 'list'}
        content = self.PostRequest(params)
        jid = content['return'][0]['jid']
        return jid



    '''saltstack key管理 action需要进行传入，方法有,accept,delete,reject'''
    def actionKeys(self,keystrings,action):
        func = 'key.' + action
        params = {'client': 'wheel', 'fun': func, 'match': keystrings}
        content = self.PostRequest(params)
        ret = content['return'][0]['data']['success']
        return ret


    '''saltstack key 批量管理传入值必须为一个字典'''

    def dictActionKeys(self,keydict,action):
        func = 'key.' + action + '_dict'
        params = {'client':'wheel','fun':func,'match':keydict}
        content = self.PostRequest(params)
        return content['return'][0]

    def cpFiletoMinions(self,tgt):
        params={'client':'local','tgt': tgt, 'fun': 'cp.get'}
        content = self.PostRequest(params)
        ret = content['return'][0]
        return ret

    #获取JOB ID的详细执行结果
    def runner(self,arg):
        ''' Return minion status '''
        params = {'client': 'runner', 'fun': arg }
        content = self.PostRequest(params)
        jid = content['return'][0]
        return jid

    def salt_runner(self, jid):
        '''
        通过jid获取执行结果
        '''

        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        print params
        content = self.PostRequest(params)
        print content
        return content['return'][0]


    #获取events
    def SaltEvents(self):
        parurl = '/events'
        res = self.PostRequest(None,parurl)
        return res

    #接受KEY
    def AcceptKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id, 'include_rejected': True, 'include_denied': True}
        content = self.PostRequest(params)
        ret = content['return'][0]['data']['success']
        return ret

    #删除KEY
    def DeleteKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        content = self.PostRequest(params)
        ret = content['return'][0]['data']['success']
        return ret

    # 拒绝KEY
    def RejectKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.reject', 'match': key_id,  'include_accepted': True, 'include_denied': True}
        content = self.PostRequest(params)
        ret = content['return'][0]['data']['success']
        return ret

    def Saltalive(self,tgt):
        '''
        salt主机存活检测
        '''

        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        content = self.PostRequest(params)
        return content['return'][0]



def format(data):
    print data


if __name__ == '__main__':
    salt=SaltApi('http://192.168.2.150:8000','roddy','roudy_123456')
    #a=salt.Softwarete_deploy('192.168.2.147,',arg=['saltenv="prod"','nginx.install,zabbix-client.install','test=True'])

    #a=salt.Softwarete_deploy('192.168.2.147',kwarg={'mods':'redis.install,nginx.install','test':True,'saltenv':'prod'})
    #print a
    #a = salt.SaltRun('192.168.2.147','state.sls','nginx.install,redis.install',saltenv='prod','test=True')
    #data=salt.Saltalive('192.168.2.147')
    #print data
    #host='192.168.2.147,192.168.2.148,'
    #data=salt.shell_remote_execution(host, 'df -i')
    #print data
    data = salt.salt_runner(20161215192828817118)
    print data
    format(data)


    #print salt.SaltRun(client='runner', fun='fileserver.envs')
    #a=sorted(salt.SaltRun(client='runner',fun='fileserver.envs')['return'][0])
    #print a
    #jids = salt.runner("jobs.list_jobs")
    #print jids
    #for i,v in jids.items:
    #    print i,v
    #a,b,c,d =salt.List_all_keys()
    #print a,b,c,d
    #salt.shell_remote_execution

    #funs = ['doc.runner', 'doc.wheel', 'doc.execution']
    #for fun in funs:
    #    result = salt.SaltRun(fun=fun, client='runner')
    #    cs = result['return'][0]
    #    for c in cs:
    #        print fun.split('.')[1], c.split('.')[0]

    #server=ServerDiskInfo(data, u'192.168.2.147')
    #server=ServerCPUInfo(data,u'192.168.2.147')
    #print server.ServerCPU()

    #data=salt.grainsall('192.168.2.147')
    #print data
     #clientkey=salt.List_all_keys()['minions']
#    Servers={}
#    for i in clientkey:
#        data=salt.grainsall(i)
#        server=ServerNICInfo(data,i)
#        serverinfo=server.ServerNIC()
#        print serverinfo






