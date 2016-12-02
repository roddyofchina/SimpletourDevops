#coding:utf8
from __future__ import unicode_literals

from django.db import models

class SaltServer(models.Model):
    Role = (
    ('Master', 'Master'),
    ('Backend', 'Backend'),
    )
    url = models.URLField(max_length=100,verbose_name=u'URL地址')
    username = models.CharField(max_length=50, verbose_name=u'用户名')
    password = models.CharField(max_length=50,verbose_name=u'密码')
    role = models.CharField(choices=Role,max_length=20,default='Master',verbose_name=u'角色')

    def __unicode__(self):
        return u"%s - %s" %(self.url,self.role)

    class Meta:
        verbose_name = u'Salt服务器'
        verbose_name_plural = u'Salt服务器列表'

class Module(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'Salt模块名称')
    def __unicode__(self):
        return "%s - %s "% (self.client,self.name)
    class Meta:
        verbose_name = u'Salt模块'
        verbose_name_plural = u'Salt模块列表'
        unique_together = ("name",)

'''
class Command(models.Model):
    cmd = models.CharField(max_length=100,verbose_name=u'Salt命令')
    doc = models.TextField(max_length=2000,blank=True,verbose_name=u'帮助文档')
    module = models.ForeignKey(Module,verbose_name=u'所属模块')

    def __unicode__(self):
        return  u"%s - %s"%(self.module,self.cmd)

    class Meta:
        verbose_name = u'Salt命令'
        verbose_name_plural = u'Salt命令列表'
        unique_together = ("module", "cmd")
'''

class Minions(models.Model):
    Status = (
    ('Unknown', 'Unknown'),
    ('Accepted', 'Accepted'),
    ('Denied', 'Denied'),
    ('Unaccepted', 'Unaccepted'),
    ('Rejected', 'Rejected'),
    )
    minion = models.CharField(max_length=50,verbose_name=u'客户端')
    saltserver = models.ForeignKey(SaltServer,verbose_name=u'所属Salt服务器')
    status = models.CharField(choices=Status,max_length=20,default='Unknown',verbose_name=u'在线状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')

    def __unicode__(self):
        return self.minion

    class Meta:
        verbose_name = u'Salt客户端'
        verbose_name_plural = u'Salt客户端列表'


class MinionStatus(models.Model):
    minion = models.ForeignKey(Minions)
    Status = (
    ('Unknown', 'Unknown'),
    ('Offline', 'Offline'),
    ('Online','Online')
    )

    minion_status = models.CharField(choices=Status,max_length=20,default='Unknown',verbose_name=u'在线状态')

class MinionGroup(models.Model):
    groupname = models.CharField(u'Minion组',max_length=50,default='default')
    minions = models.ManyToManyField(Minions,verbose_name=u'Minions',blank=True)

    def __unicode__(self):
        return self.groupname

    class Meta:
        verbose_name = u'Minion组'
        verbose_name_plural = u'Minion组'

class CmdRunLog(models.Model):
    user=models.CharField(max_length=30)
    time=models.DateTimeField()
    target=models.CharField(max_length=100)
    mapping=models.CharField(max_length=50)
    cmd=models.CharField(max_length=500)
    hosts=models.CharField(max_length=500)
    total=models.IntegerField()

    class Meta:
        verbose_name = u'命令执行日志'
        verbose_name_plural = u'命令执行日志'

class ModuleDeployLog(models.Model):
    user=models.CharField(max_length=50)
    time=models.DateTimeField()
    target=models.CharField(max_length=100)
    application=models.CharField(max_length=100)
    #成功的主机
    success_hosts=models.CharField(max_length=500)
    #失败的主机
    failed_hosts=models.CharField(max_length=500)
    #执行总共结果
    total=models.IntegerField()
    #执行过程
    log=models.TextField()
    #持续时间
    duration=models.CharField(max_length=500)
    class Meta:
        verbose_name = u'软件部署'
        verbose_name_plural = u'软件部署'