#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'
import urllib,urllib2
import json
from Assets_Module import ServerBaseInfo,ServerCPUInfo,ServerNICInfo,ServerDiskInfo


class SaltApi(object):

    __token = ''
    print __token
    def __init__(self,url,user,password):
        print url,user,password
        self.__url = url
        self.__user= user
        self.__pass = password
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
        print content
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        minions_deny = content['return'][0]['data']['return']['minions_denied']
        return minions, minions_pre, minions_rej, minions_deny


    def shell_remote_execution(self,tgt,arg):
        ''' Shell command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]
        return ret



    '''saltstack key管理 action需要进行传入，方法有,accept,delete,reject'''
    def actionKeys(self,keystrings,action):
        func = 'key.' + action
        params = {'client': 'wheel', 'fun': func, 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    '''saltstack key 批量管理传入值必须为一个字典'''


    def dictActionKeys(self,keydict,action):
        func = 'key.' + action + '_dict'
        params = {'client':'wheel','fun':func,'match':keydict}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        return content


    def SaltRun(self, fun, client='runner_async', arg=None, **kwargs):
        params = {'client': client, 'fun': fun}
        if arg:
            argslist = arg.split(',')  # 参数按逗号分隔
            for i in argslist:
                b = i.split('=')  # 每个参数再按=号分隔
                if len(b) > 1:
                    params[b[0]] = '='.join(b[1:])  # 带=号的参数作为字典传入
                else:
                    params['arg%s' % a.index(i)] = i
        if kwargs:
            params = dict(params.items() + kwargs.items())
        # print params
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res


    def cpFiletoMinions(self,tgt):
        params={'client':'local','tgt': tgt, 'fun': 'cp.get'}
        obj=urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]
        return ret

    #获取JOB ID的详细执行结果
    def runner(self,arg):
        ''' Return minion status '''
        params = {'client': 'runner', 'fun': arg }
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        jid = content['return'][0]
        return jid


    #获取events
    def SaltEvents(self):
        parurl = '/events'
        res = self.PostRequest(None,parurl)
        return res


    #接受KEY
    def AcceptKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    #删除KEY
    def DeleteKey(self, key_id):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        obj = urllib.urlencode(params)
        content = self.PostRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret



if __name__ == '__main__':
    salt=SaltApi('http://192.168.2.150:8000','roddy','roudy_123456')
    #data=salt.shell_remote_execution('192.168.2.147','df -i')
    #print salt.SaltRun(client='runner', fun='fileserver.envs')
    #a=sorted(salt.SaltRun(client='runner',fun='fileserver.envs')['return'][0])
    #print a
    jids = salt.runner("jobs.list_jobs")
    for i,v in jids.items:
        print i,v
    #a,b,c,d =salt.List_all_keys()
    #print a,b,c,d

    #funs = ['doc.runner', 'doc.wheel', 'doc.execution']
    #for fun in funs:
    #    result = salt.SaltRun(fun=fun, client='runner')
    #    cs = result['return'][0]
    #    for c in cs:
    #        print fun.split('.')[1], c.split('.')[0]

    #server=ServerDiskInfo(data, u'192.168.2.147')
    #server=ServerCPUInfo(data,u'192.168.2.147')
    #print server.ServerCPU()

#    print salt.grains('server.192.168.2.70','zmqversion')
     #clientkey=salt.List_all_keys()['minions']
#    Servers={}
#    for i in clientkey:
#        data=salt.grainsall(i)
#        server=ServerNICInfo(data,i)
#        serverinfo=server.ServerNIC()
#        print serverinfo






