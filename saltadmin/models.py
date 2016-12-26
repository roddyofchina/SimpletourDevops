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
        permissions = (
            ("salt_index_view", "Can view %s"  % verbose_name),
        )


class Modules(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'Salt模块名称')
    models_site = models.CharField(max_length=50,null=True,blank=True,verbose_name=u'Salt模块参数')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Salt软件'
        verbose_name_plural = u'Salt软件'


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
    ('Accepted', 'Accepted'),
    ('Unaccepted', 'Unaccepted'),
    ('Rejected', 'Rejected'),
    )
    minion = models.CharField(max_length=50,verbose_name=u'客户端',unique=True)
    saltserver = models.ForeignKey(SaltServer,verbose_name=u'所属Salt服务器')
    status = models.CharField(choices=Status,max_length=20,default='Unknown',verbose_name=u'Key状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')

    def __unicode__(self):
        return self.minion

    class Meta:
        verbose_name = u'Salt客户端'
        verbose_name_plural = u'Salt客户端列表'


class MinionStatus(models.Model):
    minion = models.OneToOneField(Minions)
    minion_status = models.CharField(max_length=20,verbose_name=u'在线状态')
    # 上次检测时间
    alive_time_last = models.DateTimeField(auto_now=True,null=True)
    # 当前检测时间
    alive_time_now = models.DateTimeField(auto_now=True,null=True)

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
    time=models.DateTimeField(auto_now_add=True,null=True)
    target=models.CharField(max_length=500)
    cmd=models.CharField(max_length=500)
    total=models.IntegerField()
    runsuccess = models.IntegerField(default=0)
    runerror = models.IntegerField(default=0)
    runresult = models.TextField(max_length=65535,null=True,blank=True)

    class Meta:
        verbose_name = u'命令执行日志'
        verbose_name_plural = u'命令执行日志'


class SaltJobs(models.Model):
    jid = models.CharField(max_length=50,unique=True)
    args = models.CharField(max_length=50,null=True,blank=True)
    function = models.CharField(max_length=50)
    startTime = models.CharField(max_length=100)
    target = models.CharField(max_length=500)
    user = models.CharField(max_length=50)
    saltserver = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name = u'Jobs列表'
        verbose_name_plural = u'Jobs列表'



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