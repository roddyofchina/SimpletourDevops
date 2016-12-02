from django.conf.urls import url

from saltadmin.views import (KeyList,Minion_Status,SoftInstall,JobList,RemoteCmd,SaltMasterList)

urlpatterns = [
    url(r'keylist/', KeyList, name='KeyList'),
    url(r'minion/status/',Minion_Status,name='Minion_Status'),
    url(r'minion/softinstall/',SoftInstall,name='SoftInstall'),
    url(r'job/list/',JobList,name='JobList'),
    url(r'cmd/',RemoteCmd,name='RemoteCmd'),
    url(r'master/$',SaltMasterList,name='SaltMasterList'),

]
