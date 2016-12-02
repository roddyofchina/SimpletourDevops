from django.conf.urls import url

from saltadmin.views import (KeyList,MinionStatus,SoftInstall,JobList,RemoteCmd)

urlpatterns = [
    url(r'keylist/', KeyList, name='KeyList'),
    url(r'minion/status/',MinionStatus,name='MinionStatus'),
    url(r'minion/softinstall/',SoftInstall,name='SoftInstall'),
    url(r'job/list/',JobList,name='JobList'),
    url(r'cmd/',RemoteCmd,name='RemoteCmd'),

]
