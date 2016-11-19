#coding:utf8
from __future__ import unicode_literals

from django.db import models

from servermanager.models import Server


class Dockerimage(models.Model):
    imagesId = models.CharField(u'镜像ID', max_length=64)
    repository = models.CharField(u'仓库', max_length=64,blank=True)
    tag = models.CharField(u'Tag', max_length=32,blank=True)
    imagehost = models.GenericIPAddressField(u'主机IP')
    size = models.CharField(u'大小', max_length=32,blank=True)

    update_at = models.DateTimeField(blank=True, auto_now=True,null=True)

    def __unicode__(self):
        return self.imagesId

    class Meta:
        verbose_name = u'Docker镜像'
        verbose_name_plural = u"Docker镜像"


class DockerHost(models.Model):
    host = models.OneToOneField(Server,verbose_name=u'主机')
    hostip = models.GenericIPAddressField(max_length=128,null=False,default='',verbose_name=u'docker IP地址')
    containers = models.IntegerField(u'容器数',blank=True,null=True)
    images = models.IntegerField(verbose_name=u'镜像数',blank=True,null=True)
    port = models.IntegerField(u'端口',blank=True)
    enabled = models.IntegerField(u'状态',blank=True)
    serverversion = models.CharField(u'docker版本', max_length=32,blank=True)
    datatotal = models.CharField(u'总共空间', max_length=32,blank=True)
    datause = models.CharField(u'已使用空间', max_length=32,blank=True)
    dataAvailable = models.CharField(u'剩余空间', max_length=32,blank=True)
    storageDriver = models.CharField(u'存储驱动', max_length=32,blank=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)
    def __unicode__(self):
        return self.hostip

    class Meta:
        verbose_name = u'Docker主机'
        verbose_name_plural = u"Docker主机"


class DockerContainer(models.Model):
    hostip = models.GenericIPAddressField(u'宿主机IP地址',max_length=128,blank=True,null=True)
    containerID = models.CharField(u'容器ID', max_length=64)
    Name = models.CharField(u'容器名', max_length=255,blank=True)
    command = models.CharField(u'执行命令', max_length=255,blank=True)
    status = models.CharField(u'状态', max_length=32,blank=True)
    image= models.CharField(verbose_name=u'镜像', blank=True,max_length=64)
    Created = models.DateTimeField(u'创建时间',blank=True,)
    update_at = models.DateTimeField(blank=True, auto_now=True,null=True)

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Docker容器'
        verbose_name_plural = "Docker容器"


class DockerContainerInfo(models.Model):
    containerid = models.CharField(u'容器ID', max_length=48)   #与上表进行关联
    State = models.CharField(u'状态', max_length=48)
    Driver = models.CharField(u'磁盘设备', max_length=48,blank=True,null=True)
    net = models.CharField(u'网络模式', max_length=48,blank=True)
    cpu = models.CharField(u'CPU', max_length=32,blank=True)
    mem =models.CharField(u'内存', max_length=32,blank=True)
    ip = models.GenericIPAddressField(u'IP')
    dns = models.CharField(u'DNS', max_length=32,blank=True)
    host = models.CharField(u'主机', max_length=32,blank=True)
    MacAddress = models.CharField(u'网卡mac地址', max_length=64)
    uptime = models.CharField(u'运行时间', max_length=32,blank=True)
    gateway = models.GenericIPAddressField(u'网关')



class ContainerPorts(models.Model):
    containerid = models.CharField(u'容器ID', max_length=48)   #与上表进行关联
    container_port = models.IntegerField(u'容器端口',blank=True)
    protocol = models.CharField(u'协议',max_length=32,blank=True)
    hostip = models.GenericIPAddressField(u'映射IP')
    hostport = models.CharField(u'主机端口',max_length=32,blank=True)

    def __unicode__(self):
        return self.containerid

    class Meta:
        verbose_name = u'端口管理'
        verbose_name_plural = u"端口管理"
