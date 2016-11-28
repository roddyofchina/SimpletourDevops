#coding:utf8

from django.contrib import admin
from django.forms import ModelForm,TextInput,Textarea
from django.contrib.admin import ModelAdmin

#from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
from servermanager.models import *
from import_export import resources
from django.forms import ModelForm

#导入和导出
from import_export.admin import ImportExportModelAdmin



#定义导出的内容
class ServerResource(resources.ModelResource):
    class Meta:
        model = Server

class AssetsResource(resources.ModelResource):
    class Meta:
        model = Assets

'''
class AssetsTimeForm(ModelForm):
    class Meta:
        widgets = {
            'euse_time': SuitDateWidget,
            'suse_time': SuitDateWidget,
        }'''

# Register your models here.
class AssetsAdmin(ImportExportModelAdmin):
    resource_class = AssetsResource
    #form = AssetsTimeForm
    list_display = ('id','host_name','device_type','device_number','IDC','status','business','buy_time','buy_type','price','admin')
    list_filter = ('IDC','business','status','device_type')
    search_fields = ['hostname','id']

    fieldsets = (
        ('基本信息', {'fields': ('host_name', 'device_type', 'device_number','business','buy_type', 'IDC','status', 'admin','provider',)}),
        ('其它信息', {'fields': ('Warranty','buy_time', 'suse_time', 'euse_time','price','description')}),
    )


class CpuModels(admin.ModelAdmin):
    list_display = ('id','uuid','cpu_mhz','model','Architecture')
    list_display_links = ('uuid',)
    list_editable = ('cpu_mhz',)

class DiskModels(admin.ModelAdmin):
    search_fields = ['parent_sn']
    list_display = ('id','uuid', 'capacity','disk_type','Firm')

class NicModels(admin.ModelAdmin):
    search_fields = ('ip',)
    list_display = ('id','uuid','name','ip','model')
    list_display_links = ('uuid',)

class SoftwareModels(admin.ModelAdmin):
    list_display = ('id','name','version')

class DeviceTypeModels(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id','name',)

class BusinessModels(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)
    list_editable = ('name',)

class ProviderModels(admin.ModelAdmin):
    list_display = ('id','provider_name', 'address', 'contacts', 'phone')

class ServerModels(admin.ModelAdmin):
    list_display = ('id','Assets','Firm','cpu','hostname','saltid','mem','swap','system','version','platform')
    list_display_links = ('Assets',)

    def get_idc(self, obj):
        return obj.Assets.IDC
    get_idc.short_description = '资产'

    filter_horizontal = ('disk','nic','software')

class IdcModels(admin.ModelAdmin):
    search_fields = ('idc_name',)
    list_display = ('idc_name','address','floor','contacts','phone')


admin.site.register(Assets,AssetsAdmin)
admin.site.register(Server,ServerModels)
admin.site.register(DeviceType,DeviceTypeModels)
admin.site.register(Business,BusinessModels)
admin.site.register(Cpu,CpuModels)
admin.site.register(Disk,DiskModels)
admin.site.register(IDC,IdcModels)
admin.site.register(Software,SoftwareModels)
admin.site.register(NIC,NicModels)
admin.site.register(Provider,ProviderModels)



