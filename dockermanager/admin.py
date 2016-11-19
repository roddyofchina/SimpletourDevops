#coding:utf8
from django.contrib import admin
from dockermanager.models import *
class DockerHostModels(admin.ModelAdmin):
    list_display = ('host','containers','images','port','enabled')
class DockerContainerModels(admin.ModelAdmin):
    list_display = ('Name','status','ip','host','uptime')
admin.site.register(DockerHost,DockerHostModels)
admin.site.register(DockerContainer)
admin.site.register(Dockerimage)


