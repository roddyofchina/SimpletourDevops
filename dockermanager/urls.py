from django.conf.urls import url

from dockermanager.views import (Dockercontainerlist,DockerHosts,DockerImages,DockercontainerSearch,
                                 DockerHostAdd,DockerHostDel,DockerHostEdit,DockerContainerDel,
                                 DockerContainerStop,DockerContainerStart,DockerContainerRestart,
                                 DockerImageDelete,DockerLogOutput,StartCeleryStatus,StopCeleryStatus,
                                 RestartCeleryStatus,DeleteCeleryStatus,webSocket,getsocket)

urlpatterns = [
    url(r'container/list/(\d+)$', Dockercontainerlist, name='Dockercontainerlist'),
    url(r'container/search/(?P<page>\d+)$',DockercontainerSearch,name='DockercontainerSearch'),
    url(r'container/restart/(\w+)$',DockerContainerRestart,name='DockerContainerRestart'),
    url(r'container/stop/(\w+)$', DockerContainerStop,name='DockerContainerStop'),
    url(r'container/start/(\w+)$', DockerContainerStart, name='DockerContainerStart'),
    url(r'container/logs/(\w+)$',DockerLogOutput,name='DockerLogOutput'),
    url(r'container/delete/(\w+)$',DockerContainerDel,name='DockerContainerDel'),
    url(r'container/start/task/(\w+\-\w+\-\w+\-\w+\-\w+)$',StartCeleryStatus,name='StartCeleryStatus'),
    url(r'container/restart/task/(\w+\-\w+\-\w+\-\w+\-\w+)$',RestartCeleryStatus,name='RestartCeleryStatus'),
    url(r'container/stop/task/(\w+\-\w+\-\w+\-\w+\-\w+)$',StopCeleryStatus,name='StopCeleryStatus'),
    url(r'container/delete/task/(\w+\-\w+\-\w+\-\w+\-\w+)$',DeleteCeleryStatus,name='DeleteCeleryStatus'),
    url(r'server/list/$', DockerHosts, name='DockerHosts'),
    url(r'images/list/(\d+)$',DockerImages, name='DockerImages'),
    url(r'images/del/(\d+)$', DockerImageDelete, name='DockerImageDelete'),
    url(r'server/add/$', DockerHostAdd, name='DockerHostAdd'),
    url(r'server/del/(\d+)$',DockerHostDel,name='DockerHostDel'),
    url(r'server/edit/(\d+)$',DockerHostEdit,name='DockerHostEdit'),
    url(r'webSocket/(\w+)$',webSocket,name='webSocket'),
    url(r'getSocket/(\w+)$',getsocket,name='getsocket'),
]
