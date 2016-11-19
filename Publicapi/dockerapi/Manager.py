#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

import docker


'''
Docker 容器API公共模块，可进行容器及镜像管理
'''

class Dockerapi(object):
    def __init__(self, host, port):
        self.dockerConnect = docker.Client(base_url='tcp://%s:%s' %(host,port), timeout=60, version='1.22')

    def GetallContainers(self):
        Containers = self.dockerConnect.containers(all=1)
        return Containers

    def SearchContainers(self, Searchparameter):
        SearchContainer = self.dockerConnect.containers(all=1,filters={'name':[Searchparameter]})
        return SearchContainer

    def ContainerStatus(self, Status):
        StatusContainer = self.dockerConnect.containers(all=1,filters={'status':[Status]})
        return StatusContainer

    def InspectContainer(self,name):
        inspect = self.dockerConnect.inspect_container(container=name)
        return inspect


    def Dockerversion(self):
        Version = self.dockerConnect.version()
        return Version

    def StartContainer(self, name):
        StartContainer = self.dockerConnect.start(container=name)
        return StartContainer

    def StopContainer(self, name):
        StopContainer = self.dockerConnect.stop(container=name)
        return StopContainer

    def DelayedstopContainer(self, name, timeout):
        delayedstop = self.dockerConnect.stop(container=name, timeout=timeout)
        return delayedstop

    def Dockerinfo(self):
        dockerinfo = self.dockerConnect.info()
        return dockerinfo

    def RestartContainer(self, name):
        restart = self.dockerConnect.restart(container=name)
        return restart

    def DelayedRestart(self, name, timeout):
        delayedrestart = self.dockerConnect.restart(container=name, timeout=timeout)
        return delayedrestart

    def RenameDocker(self, name, newname):
        rename = self.dockerConnect.rename(container=name, name=newname)
        return rename

    def TopContainer(self, name):
        topinfo = self.dockerConnect.top(container=name, ps_args=aux)
        return topinfo

    def killContainer(self, name):
        kill = self.dockerConnect.kill(container=name)
        return kill

    def PauseContainer(self, name):
        pause = self.dockerConnect.pause(container=name)
        return pause

    def UnpauseContainer(self, name):
        unpause = self.dockerConnect.unpause(container=name)
        return unpause

    def removeContainer(self, name, v=False, link=False, force=False):
        remove = self.dockerConnect.remove_container(container=name, v=v, link=link, force=force)
        return remove

    def LogContainer(self,name,timestamps=False,tail=all):

        logs = self.dockerConnect.logs(container=name,stdout=True,stderr=True,timestamps=timestamps,tail=tail)

        return logs


    def AllImages(self):
        images=self.dockerConnect.images(all=1)
        return images

    def DeleteImages(self,imagename):

        data=self.dockerConnect.remove_image(image=imagename,force=False)

        return u"删除镜像成功!!"



if __name__ == '__main__':
    test=Dockerapi('192.168.2.232','2375')
    #a=test.DeleteImages('docker.io/centos/v1:latest')
    #print a

    # search=test.SearchContainers('simpletou')
    # status=test.ContainerStatus('exited')
    # version=test.Dockerversion()
    # stop=test.StopContainer('nostalgic_albattani')
    #tart=test.StartContainer('nostalgic_albattani')
    #stopd=test.DelayedstopContainer('nostalgic_albattani',10)
    #print stopd
    #rename=test.RenameDocker('nostalgic_albattani','aaa')
    #inspect = test.InspectContainer('aaa')
    #print all














