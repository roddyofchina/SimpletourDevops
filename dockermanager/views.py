#coding:utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect

from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from dockermanager.models import DockerHost,Dockerimage,DockerContainer

# Create your views here.
from webapp.Extends import PageList
from servermanager.models import Server
from dockermanager import forms
from Publicapi.dockerapi.Manager import Dockerapi
from webapp.tasks import StopContainer,StartContainer,RestartContainer,DeleteContainer
import  json
import docker
from webapp.models import *

@login_required()
def Dockercontainerlist(request,page):
    usersession=request.session.get('user_id')
    if request.method == 'POST':
        searchdata = request.POST.get('search')
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = DockerContainer.objects.filter(Q(containerID__contains=searchdata) | Q(Name__contains=searchdata)).count()
        result = DockerContainer.objects.filter(Q(containerID__contains=searchdata) | Q(Name__contains=searchdata)).order_by('-id')[start:end]
        url = "/docker/container/list"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)

        ret = {'Containerdata': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request,'dockermanager/containers_list.html',ret)

    else:
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = DockerContainer.objects.all().count()
        result = DockerContainer.objects.all().order_by('-id')[start:end]
        url = "/docker/container/list"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)

        ret = {'Containerdata': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request,'dockermanager/containers_list.html',ret)



@login_required()
def DockercontainerSearch(request,page):
    usersession=request.session.get('user_id')
    if request.method == 'GET':
        searchdata = request.GET.get('search')
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = DockerContainer.objects.filter(Q(containerID__contains=searchdata) | Q(Name__contains=searchdata)).count()
        result = DockerContainer.objects.filter(Q(containerID__contains=searchdata) | Q(Name__contains=searchdata)).order_by('-id')[start:end]
        url = "/docker/container/search"
        search=u"?search=%s" %searchdata
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count,search)

        ret = {'Containerdata': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request,'dockermanager/containers_list.html',ret)




@login_required()
def DockerHosts(request):
    usersession=request.session.get('user_id')
    if request.method == 'POST':
        id = request.POST['id']
        status= request.POST['checkboxValue']
        if status == 'true':
            status=1
        else:
            status=0
        dockerhostdata = DockerHost.objects.get(id=id)
        dockerhostdata.enabled = status
        dockerhostdata.save()
        msg={'msginfo':u'主机状态修改成功!!!!!!'}
        return HttpResponse(json.dumps(msg))
    else:
        Hostadata=DockerHost.objects.all()
        ret={'usersession':usersession,'Hostadata':Hostadata}
        return  render(request,'dockermanager/dockerhosts_list.html',ret)


@login_required()
def DockerHostAdd(request):

    username = request.session.get('user_name')
    restdata = {'data':'','regerror':'','usersession': request.session.get('user_id')}
    registerobj=forms.DockerServerAdd()
    restdata['data'] = registerobj

    listdata=[]
    [listdata.append(int(i.host.id)) for i in DockerHost.objects.all()]
    ServerData=Server.objects.exclude(id__in=listdata)
    restdata['ServerData']=ServerData

    if request.method == 'POST':
        form = forms.DockerServerAdd(request.POST)
        if form.is_valid():
            ServerData = request.POST['DockerServer']
            ServerData = Server.objects.get(id=ServerData)
            dockerip = request.POST['dockerip']
            dockerport = request.POST['dockerport']
            ServerStatus = int(request.POST['ServerStatus'])

            NewDockerHost=DockerHost(host=ServerData,hostip=dockerip,port=dockerport,enabled=ServerStatus)
            NewDockerHost.save()
            Operation.objects.create(Opuser=username,Opaction=u'添加Docker宿主机')
            return HttpResponseRedirect('/docker/server/list/')
        else:
            restdata['data'] = form
    return render(request,'dockermanager/dockerhosts_add.html', restdata)

@login_required()
def DockerImages(request,page):
    usersession=request.session.get('user_id')
    if request.method == 'POST':
        pass
    else:
         #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Dockerimage.objects.all().count()
        result = Dockerimage.objects.all().order_by('-id')[start:end]
        url = "/docker/images/list"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)

        ret = {'Imagedata': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request,'dockermanager/images_list.html',ret)

@login_required()
def DockerImageDelete(request, imageid):
    username = request.session.get('user_name')
    if request.method == 'GET':
        Image=Dockerimage.objects.get(id=imageid)
        if Image:
            repo=Image.repository
            #查询DOCKER主机IP及端口
            ip = Image.imagehost
            port = DockerHost.objects.get(hostip=ip).port
            dockerapi = Dockerapi(ip,port)
            a=dockerapi.DeleteImages(repo)
            Image.delete()
            Operation.objects.create(Opuser=username,Opaction=u'删除Docker镜像 %s' %repo)
            return HttpResponse(a)
        else:
            return HttpResponse(u"没有该镜像!!")

@login_required()
def DockerHostDel(request,hostid):
    username = request.session.get('user_name')
    if request.method == 'GET':
       DockerHost.objects.get(id=hostid).delete()
       Operation.objects.create(Opuser=username,Opaction=u'删除Docker宿主机%s' %hostid)
       msg={'msginfo':u'DockerHost 删除成功!!!'}
       return HttpResponse(json.dumps(msg))

@login_required()
def DockerHostEdit(request,hostid):
    usersession=request.session.get('user_id')
    username = request.session.get('user_name')
    HostData=DockerHost.objects.get(id=hostid)
    if request.method == 'POST':
        pass
        Operation.objects.create(Opuser=username,Opaction=u'修改Docker宿主机%s' %hostid)
    else:
        listdata=[]
        [listdata.append(int(i.host.id)) for i in DockerHost.objects.all()]
        hostid=HostData.host.id
        listdata.remove(hostid)
        ServerData=Server.objects.exclude(id__in=listdata)

        ret={'usersession':usersession,'HostData':HostData,'hostid':hostid,'ServerData':ServerData}
        return render(request,'dockermanager/dockerhosts_edit.html', ret)

@login_required()
def DockerContainerStop(request,containerid):
    username = request.session.get('user_name')
    if request.method == 'GET':
        IP=DockerContainer.objects.get(containerID=containerid).hostip
        port = DockerHost.objects.get(hostip=IP).port
        a=StopContainer.delay(dict(host=IP,port=port,container=containerid))
        Operation.objects.create(Opuser=username,Opaction=u'停止容器%s' %containerid[0:12])
        msg={'celeryId':a.id}
        return HttpResponse(json.dumps(msg))

@login_required()
def DockerContainerRestart(request,containerId):
    username = request.session.get('user_name')
    if request.method == 'GET':
        IP=DockerContainer.objects.get(containerID=containerId).hostip
        port = DockerHost.objects.get(hostip=IP).port
        a=RestartContainer.apply_async((IP, port, containerId))
        Operation.objects.create(Opuser=username,Opaction=u'重启容器%s' %containerId[0:12])
        msg={'celeryId':a.id}
        return HttpResponse(json.dumps(msg))

@login_required()
def DockerContainerDel(request,containerId):
    username = request.session.get('user_name')
    if request.method == 'GET':
        print "sdsdsds"
        IP=DockerContainer.objects.get(containerID=containerId).hostip
        port = DockerHost.objects.get(hostip=IP).port
        print "ssssssss"
        print IP,port,containerId
        a=DeleteContainer.apply_async((IP, port, containerId))
        Operation.objects.create(Opuser=username,Opaction=u'删除容器%s' %containerId[0:12])
        msg={'celeryId': a.id}
        return HttpResponse(json.dumps(msg))

@login_required()
def DockerContainerStart(request, containerId):
    username = request.session.get('user_name')
    if request.method == 'GET':
        IP=DockerContainer.objects.get(containerID=containerId).hostip
        port = DockerHost.objects.get(hostip=IP).port
        a=StartContainer.apply_async((IP, port, containerId))
        Operation.objects.create(Opuser=username,Opaction=u'启动容器%s' %containerId[0:12])
        msg={'celeryId': a.id}
        return HttpResponse(json.dumps(msg))


@login_required()
def DockerLogOutput(request,containerid):
    usersession=request.session.get('user_id')
    if request.method == 'GET':
        IP=DockerContainer.objects.get(containerID=containerid).hostip
        port = DockerHost.objects.get(hostip=IP).port
        try:
            dockerserver = Dockerapi(IP,port)
            data=dockerserver.LogContainer(containerid,tail=30)
            data=data.split('\n')
        except docker.errors.NotFound:
            return HttpResponse('没有该容器')
        ret = {'usersession': usersession,'dockerlogsdata':data,'containerid':containerid}
        return render(request,'dockermanager/dockerhosts_logs.html',ret)
    else:
        IP=DockerContainer.objects.get(containerID=containerid).hostip
        port = DockerHost.objects.get(hostip=IP).port
        try:
            dockerserver = Dockerapi(IP,port)
            data=dockerserver.LogContainer(containerid,tail=30)
            data=data.split('\n')
        except docker.errors.NotFound:
            return HttpResponse('没有该容器')
        ret={'dockerlogsdata':data}
        return HttpResponse(json.dumps(ret))

@login_required()
def StartCeleryStatus(request,celeryid):
    if request.method == 'GET':
        task=StartContainer.AsyncResult(str(celeryid))
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': task.status,
            }
            if 'result' in task.info:
                response['result'] = task.info['result']

        else:
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return HttpResponse(json.dumps(response))

@login_required()
def StopCeleryStatus(request,celeryid):
    if request.method == 'GET':

        task=StopContainer.AsyncResult(str(celeryid))
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': task.status,
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return HttpResponse(json.dumps(response))

@login_required()
def RestartCeleryStatus(request,celeryid):
    if request.method == 'GET':

        task=RestartContainer.AsyncResult(str(celeryid))
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': task.status,
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            response = {
                'state': task.state,
                'status': str(task.info),  # this is the exception raised
            }
        return HttpResponse(json.dumps(response))

@login_required()
def DeleteCeleryStatus(request,celeryid):
    if request.method == 'GET':
        task=DeleteContainer.AsyncResult(str(celeryid))
        containerID=request.GET['containerid']
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            DockerContainer.objects.filter(containerID=containerID).delete()
            response = {
                'state': task.state,
                'status': task.status,
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            response = {
                'state': task.state,
                'status': str(task.info),  # this is the exception raised
            }
        return HttpResponse(json.dumps(response))



