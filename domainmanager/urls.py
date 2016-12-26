from django.conf.urls import url


from domainmanager.views import (SimpletourDomainLists,SimpletourGetdomainApi,Simpletourrecord,SimpletourGetRecords)

urlpatterns = [
    url(r'list/$', SimpletourDomainLists, name='SimpletourDomainLists'),
    url(r'dnspodapi/$',SimpletourGetdomainApi,name='SimpletourGetdomainApi'),
    url(r'records/$',SimpletourGetRecords,name='SimpletourGetRecords'),
    url(r'record/search/(?P<id>\d+)$',Simpletourrecord,name='Simpletourrecord'),
]
