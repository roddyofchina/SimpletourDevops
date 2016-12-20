from django.contrib import admin
from saltadmin.models import *

class SaltJobsModels(admin.ModelAdmin):
    list_display = ('jid','args','function','target','startTime','saltserver','user')
    search_fields = ('function','jid')


class CmdRunLogModels(admin.ModelAdmin):
    list_display = ('user','time','target','cmd','total','runsuccess','runerror')
    search_fields = ('user','cmd')


admin.site.register(SaltJobs,SaltJobsModels)
admin.site.register(CmdRunLog,CmdRunLogModels)
admin.site.register(MinionGroup)
