#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimpletourDevops.settings")
import django
django.setup()
from dockermanager.models import DockerHost,Dockerimage,DockerContainer
from Publicapi.dockerapi.Manager import Dockerapi
import time

'''获取数据'''
def GetDockerServerinfo():
    DockerServerList = DockerHost.objects.filter(enabled=1)
    for server in DockerServerList:
        try:
            docker=Dockerapi(server.hostip,server.port)
            Dockerdata=docker.GetallContainers()
            for container in Dockerdata:
                '''获取容器最新状态进行修改'''
                if DockerContainer.objects.filter(containerID=container['Id']):
                    OldContainer = DockerContainer.objects.get(containerID=container['Id'])
                    OldContainer.Name=container['Names'][0].lstrip('/')
                    OldContainer.command=container['Command']
                    OldContainer.status=container['Status']
                    OldContainer.image=container['Image']
                    OldContainer.hostip=server.hostip
                    OldContainer.Created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(container['Created']))
                    OldContainer.save()
                else:
                    '''如果没有容器就添加'''
                    NewContainer=DockerContainer(containerID=container['Id'],
                                    Name=container['Names'][0].lstrip('/'),
                                    command=container['Command'],
                                    status=container['Status'],
                                    image=container['Image'],
                                    hostip=server.hostip,
                                    Created=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(container['Created'])))
                    NewContainer.save()
        except:
            print "sssssss"
            return u"Connect Docker host is Error!!!"
    return u"OK"


def GetDockerImages():
    DockerServerList = DockerHost.objects.filter(enabled=1)
    for server in DockerServerList:
        try:
            docker=Dockerapi(server.hostip,server.port)
            DockerImagesdata=docker.AllImages()
        except:
            return u"Connect Docker host is Error!!!"
        else:
            for image in DockerImagesdata:

                if image['RepoTags'][0] == '<none>:<none>':
                    continue
                imageid=image['Id'].split(':')[-1]
                for repo in image['RepoTags']:
                    if Dockerimage.objects.filter(repository=repo):
                        Oldimage = Dockerimage.objects.get(repository=repo)
                        Oldimage.repository = repo
                        Oldimage.imagesId=imageid
                        Oldimage.tag = repo.split(':')[-1]
                        Oldimage.imagehost = server.hostip
                        Oldimage.size = image['Size']
                        Oldimage.save()
                    else:
                        Newimage=Dockerimage(imagesId=imageid,
                                    repository=repo,
                                    tag = repo.split(':')[-1],
                                    imagehost = server.hostip,
                                    size=image['Size'],
                                    )
                        Newimage.save()

    return "Get all imgeas is oK!!"


if __name__ == '__main__':
    GetDockerImages()







