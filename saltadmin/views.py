#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from saltadmin.models import *
from Publicapi.saltstackapi.SaltConApi import SaltApi
import json
from saltadmin.forms import CheckSaltServer,KeyManager





@login_required()
def SaltMasterList(request):
    usersession = request.session.get('user_id')
    if request.method == 'POST':
        SaltServerForms = CheckSaltServer(request.POST)
        print SaltServerForms
        if SaltServerForms.is_valid():
            SaltServerForms.save()
            return HttpResponse("添加成功!!!")
    else:
        SaltServerForms = CheckSaltServer()
    SaltMasterData = SaltServer.objects.all()
    return render(request, 'saltadmin/saltmaster_list.html', locals())





@login_required()
def KeyList(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        Accepted = Minions.objects.filter(status='Accepted')
        Unaccepted = Minions.objects.filter(status='Unaccepted')
        Rejected = Minions.objects.filter(status='Rejected')
        froms=KeyManager()
        return render(request,'saltadmin/key_list.html',locals())


    if request.method == 'POST':
        minion = request.POST.get('minion')
        status = request.POST.get('status')
        Minion_data=Minions.objects.get(minion=minion)
        Minion_data.status = status
        Minion_data.save()
        url = Minion_data.saltserver.url

        username = Minion_data.saltserver.username
        password = Minion_data.saltserver.password

        salt = SaltApi(url, username, password)
        if status == 'Accepted':
            ret = salt.AcceptKey(minion)
        elif status == 'Unaccepted':
            ret = salt.DeleteKey(minion)
        elif status == 'Rejected':
            ret = salt.RejectKey(minion)

        return HttpResponse('OK')


@login_required()
def Minion_Status(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        SaltMinionData = MinionStatus.objects.all()
        return render(request,'saltadmin/minion_status.html',locals())


@login_required()
def SoftInstall(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        SoftModuleData = Module.objects.all()
        GroupData = MinionGroup.objects.all()
        return render(request,'saltadmin/saltmodule_deploy.html',locals())


@login_required()
def JobList(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        return render(request,'saltadmin/saltjob_list.html',locals())



@login_required()
def RemoteCmd(request):
    usersession = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if request.method == 'GET':
        GroupData = MinionGroup.objects.all()
        #hosts = """[ {type: 1, list: [{ text: 'yang', id: 1}, {text: 'asdasd',id: 4}]}, }]"""

        groupall=[]
        for g in GroupData:
            group={}
            list = []
            for m in g.minions.all():
                dir = {}
                dir['text']  = m.minion
                dir['id'] = m.minion
                list.append(dir)

            group['type'] = g.id
            group['list'] = list
            groupall.append(group)
        groupall=json.dumps(groupall)
        return render(request,'saltadmin/salt_cmd.html',locals())

    else:
        if not request.POST.get('minion'):
            minions_id = request.POST.get('minion_group')
            minions_data=MinionGroup.objects.get(id=minions_id).minions.all()

        else:
            minions_data = request.POST.getlist('minion')

        minions_list = ''
        for m in minions_data:
            minions_list += str(m) + ','
        minions_list = minions_list.strip(',')


        cmd =request.POST.get('cmd')
        #必须是同一台master上的才能为一个组，这样只需要查询一个就可

        saltm = Minions.objects.get(minion=minions_list.split(',')[0])
        url = saltm.saltserver.url
        username = saltm.saltserver.username
        password = saltm.saltserver.password

        salt = SaltApi(url, username, password)
        jid = salt.shell_remote_execution(minions_list, cmd)

        savelog = CmdRunLog.objects.create(user=user_name, target=minions_list, cmd=cmd, total=len(minions_list.split(',')))


        ret={'jid':jid,'minion':minions_list,'savelogid':savelog.id}
        return  HttpResponse(json.dumps(ret))





@login_required()
def CmdResult(request,jid):
    if request.method == 'GET':
        minions_list = request.GET.get('minion')
        savelogid = request.GET.get('savelogid')

        saltm = Minions.objects.get(minion=minions_list.split(',')[0])
        url = saltm.saltserver.url
        username = saltm.saltserver.username
        password = saltm.saltserver.password

        salt = SaltApi(url,username,password)
        resultdata = salt.salt_runner(jid)

        print savelogid
        logs = CmdRunLog.objects.get(id=savelogid)
        logs.runresult=resultdata
        logs.runsuccess=len(resultdata)
        logs.save()

        ret={'minion':minions_list,'resultdata':resultdata}

        return HttpResponse(json.dumps(ret))



@login_required()
def SaltMinionGrains(request):
    id = request.GET.get('minion')
    action =  request.GET.get('action')
    Minion_data=MinionStatus.objects.get(id=id)
    url = Minion_data.minion.saltserver.url
    username = Minion_data.minion.saltserver.username
    password = Minion_data.minion.saltserver.password
    salt = SaltApi(url,username,password)

    if str(action) == 'grains':
        Data = salt.grainsall(str(Minion_data.minion))
    elif str(action) == 'pillar':
        Data = salt.pillarall(str(Minion_data.minion))
    else:
        Data={"msg": '无法查询'}
    return HttpResponse(json.dumps(Data))




