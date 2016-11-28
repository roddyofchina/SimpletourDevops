#coding:utf8
from __future__ import unicode_literals
from django.db import models
from webapp.models import Suser


'''设备类型表'''
class DeviceType(models.Model):
    name = models.CharField(max_length=128,verbose_name=u'设备类型')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'设备类型'
        verbose_name_plural = u"设备类型"
        permissions = (

            ("cmdb_devicetype_view", "Can view %s" %verbose_name),

        )

'''IDC信息管理表'''
class IDC(models.Model):
    idc_name = models.CharField(u'IDC',max_length=128, unique=True)
    address = models.CharField(u'地址',max_length=255, null=True,blank=True)
    floor = models.CharField(u'楼层',max_length=20,null=True,blank=True)
    contacts = models.CharField(u'联系人',max_length=128, null=True,blank=True)
    phone = models.CharField(u'联系电话',max_length=20,null=True,blank=True)

    def __unicode__(self):
        return self.idc_name

    class Meta:
        verbose_name = u'IDC'
        verbose_name_plural = u'IDC'
        permissions = (
            ("cmdb_idc_view", "Can view %s" %verbose_name),
        )
'''业务表'''
class Business(models.Model):
    name = models.CharField(max_length=128,unique=True,verbose_name=u'业务名')
    memo = models.CharField(u'备注',max_length=64, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'业务列表'
        verbose_name_plural = u'业务列表'
        permissions = (

            ("cmdb_devicetype_view", "Can view %s" %verbose_name),

        )

'''提供商表'''
class Provider(models.Model):
    provider_name = models.CharField(max_length=128,  unique=True, verbose_name=u'提供商')
    address = models.CharField(max_length=255, blank=True, verbose_name=u'地址')
    contacts = models.CharField(max_length=128, blank=True, verbose_name=u'联系人')
    phone = models.CharField(max_length=20,blank=True, verbose_name=u'联系电话')
    Fax = models.CharField(max_length=20,blank=True, verbose_name=u'传真')

    def __unicode__(self):
        return self.provider_name

    class Meta:
        verbose_name = u'供应商'
        verbose_name_plural = u'供应商'
        permissions = (
            ("cmdb_provider_view", "Can view %s" %verbose_name),
        )
'''资产表'''
class Assets(models.Model):

    host_name = models.CharField(verbose_name=u'设备名',max_length=128,null=True, unique=True)

    device_number = models.CharField(u'设备编号',max_length=128, unique=True)

    device_type = models.ForeignKey('DeviceType',verbose_name=u'设备类型',null=True,blank=True)

    #保修期
    Warranty = models.SmallIntegerField(u'保修期')

    IDC = models.ForeignKey('IDC', null=True,blank=True)

    business = models.ForeignKey('Business',verbose_name=u'业务', null=True,blank=True)

    buy_time = models.CharField(u'购买日期', max_length=128, blank=True)

    buy_type_choice = (
        (1, u'公司内购'),
        (2, u'员工自购'),
    )



    buy_type = models.SmallIntegerField(u'购买方式',choices=buy_type_choice,blank=True)

    price = models.IntegerField(u'购买价格',blank=True)


    #管理员,可以是多个管理员进行维护
    admin = models.ForeignKey(Suser, verbose_name=u'管理员邮箱',null=True,blank=True)

    suse_time = models.DateField(u'开始使用时间', max_length=128, null=True)

    euse_time = models.DateField(u'截至使用时间', max_length=128, null=True)

    status_choice = (
        (1, u'正在使用'),
        (2, u'未使用'),
        (3, u'设备故障'),
        (4, u'库存备用'),
    )

    status =models.SmallIntegerField(u'状态',choices=status_choice,blank=True)

    create_time = models.DateTimeField(u'资产创建时间', auto_now_add=True,null=True)

    devicetag = models.CharField(max_length=255, blank=True)

    #提供商
    provider = models.ForeignKey('Provider',verbose_name=u'提供商', null=True,blank=True)

    #其它备注
    description = models.TextField(max_length=255,blank=True,verbose_name=u'备注')

    def __unicode__(self):
        return self.host_name

    class Meta:
        verbose_name = u'资产表管理'
        verbose_name_plural = u'资产表管理'
        permissions = (

            ("cmdb_assets_view", "Can view %s" %verbose_name),

            ("assets_index_view", "资产管理"),
        )

'''软件版本'''
class Software(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'软件名称')
    version = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'版本')
    license = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'序列号')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'软件管理'
        verbose_name_plural = u'软件管理'
        permissions = (

            ("cmdb_software_view", "Can view %s" %verbose_name),

        )
'''服务器主表'''
class Server(models.Model):
    Assets = models.OneToOneField('Assets',verbose_name=u'资产关联',null=True,blank=True,related_name='pub')

    sn = models.CharField(max_length=128,verbose_name=u'SN号',unique=True)

    hostname = models.CharField(max_length=128,verbose_name=u'主机名')

    mem = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'内存总容量')

    swap = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'swap容量')

    platform = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'平台')

    system = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'系统')

    version = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'版本')

    #产商
    Firm = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'制造商')


    #软件安装列表
    software  = models.ManyToManyField('Software', blank=True,verbose_name=u'软件列表')

    #CPU
    cpu = models.ForeignKey('Cpu',blank=True,null=True)

    cpu_count = models.SmallIntegerField(u'cpu个数',blank=True,default=0)

    cpu_core_count = models.SmallIntegerField(u'cpu核数',blank=True,default=0)

    #nic
    nic = models.ManyToManyField('NIC', verbose_name=u'网卡列表',blank=True,null=True)

    #磁盘
    disk = models.ManyToManyField('Disk', verbose_name=u'硬盘',blank=True)

    #raid
    raid = models.CharField(max_length=128,null=True,blank=True,verbose_name=u'RAID级别')

    saltid = models.CharField(max_length=128,verbose_name=u'SaltID名')

    create_time = models.DateTimeField(blank=True, auto_now_add=True)

    add_type_choice = (
        (1,u'手动添加'),
        (2,u'自动采集'),
    )
    addtype =models.SmallIntegerField(u'采集模式',choices=add_type_choice,blank=True,default=1)

    #修改时间
    update_time = models.DateTimeField(blank=True, auto_now=True, null=True)

    def __unicode__(self):
        return "%s %s" %(self.sn, self.Assets.host_name)

    class Meta:
        verbose_name = u'服务器管理'
        verbose_name_plural = '服务器管理'
        permissions = (

            ("cmdb_server_view", "Can view %s" %verbose_name),

        )
class Cpu(models.Model):
    uuid = models.CharField(u'UUID号',max_length=64)

    parent_sn = models.CharField(max_length=128, verbose_name=u'服务器SN')

    #cpu架构
    Architecture = models.CharField(max_length=128,blank=True,null=True,verbose_name=u'架构')

    #产商
    Vendor = models.CharField(max_length=128,blank=True,null=True,verbose_name=u'制造商')

    #型号
    model = models.CharField(max_length=128,blank=True,null=True,verbose_name=u'型号')

    cpu_mhz = models.CharField(max_length=128,blank=True,null=True,verbose_name=u'频率')

    L1cache = models.CharField(max_length=128,blank=True,null=True)

    L2cache = models.CharField(max_length=128,blank=True,null=True)

    L3cache = models.CharField(max_length=128,blank=True,null=True)

    Thread = models.SmallIntegerField(null=True,verbose_name=u'线程')

    create_time = models.DateTimeField(blank=True, auto_now_add=True)

    update_time = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return self.parent_sn

    class Meta:
        verbose_name = u'CPU'
        verbose_name_plural = u'CPU'
class Disk(models.Model):
    name  = models.CharField(max_length=128,verbose_name=u'硬盘名称')

    uuid = models.CharField(max_length=128,unique=True)

    parent_sn = models.CharField(max_length=128,verbose_name=u'服务器SN')

    #产商
    Firm = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'制造商')

    #容量
    capacity = models.CharField(max_length=128,null=True, blank=True,verbose_name=u'容量')

    type_choice = (
        (1, u'SATA'),
        (2, u'SSD'),
    )

    #磁盘类型
    disk_type = models.SmallIntegerField(choices=type_choice,null=True,blank=True,verbose_name='磁盘类型')



    create_time = models.DateTimeField(blank=True, auto_now_add=True)

    update_time = models.DateTimeField(blank=True, auto_now=True)

    tag = models.CharField(max_length=128,blank=True,null=True)

    def __unicode__(self):
        return self.parent_sn


    class Meta:
        verbose_name = u'硬盘'
        verbose_name_plural = u'硬盘'
class NIC(models.Model):
    uuid = models.CharField(u'UUID号',max_length=128,)
    parent_sn = models.CharField(max_length=128,verbose_name=u'服务器SN')
    name = models.CharField(u'网卡名称', max_length=128,)
    model = models.CharField(max_length=128,blank=True,null=True,verbose_name=u'型号')
    ip = models.GenericIPAddressField(max_length=128,null=False,default='',verbose_name=u'IP地址')
    mac = models.CharField(u'mac地址', max_length=64)
    netmask = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'子网掩码')
    nicstatus = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'网卡状态')
    create_time = models.DateTimeField(blank=True, auto_now_add=True)
    update_time = models.DateTimeField(blank=True, auto_now=True)
    tag = models.CharField(max_length=128,blank=True,null=True)


    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u'网卡'



