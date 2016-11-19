from django.conf.urls import url


from servermanager.views import (HostLists,ServerDetail,ChangeServer,
                                 AssetsLists,CeleryStatus,
                                 AssetsDetail,
                                 ServerList,
                                 DeleteAsset,
                                 DeleteServer,
                                 UpdateServer,
                                 ChangeAsset,)

urlpatterns = [
    url(r'assets/(\d+)$', AssetsLists, name='AssetsLists'),
    url(r'assets/detail/(\d+)$', AssetsDetail, name='AssetsDetail'),
    url(r'assets/delete/(\d+)$', DeleteAsset, name='DeleteAsset'),
    url(r'assets/change/(\d+)$', ChangeAsset, name='ChangeAsset'),

    url(r'servers/detail/(\d+)$',ServerDetail,name='ServerDetail'),
    url(r'servers/(\d+)$', ServerList, name='ServerList'),
    url(r'servers/delete/(\d+)$', DeleteServer, name='DeleteServer'),
    url(r'servers/update/(\d+)$',UpdateServer,name='UpdateServer'),
    url(r'servers/change/(\d+)$',ChangeServer,name='ChangeServer'),
    url(r'servers/task/(\w+\-\w+\-\w+\-\w+\-\w+)$',CeleryStatus,name='CeleryStatus'),
]
