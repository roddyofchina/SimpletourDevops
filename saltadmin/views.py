from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from saltadmin.models import *



@login_required()
def SaltMasterList(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        SaltMasterData = SaltServer.objects.all()
        return render(request,'saltadmin/saltmaster_list.html',locals())

@login_required()
def KeyList(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        return render(request,'saltadmin/key_list.html',locals())


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
        return render(request,'saltadmin/saltmodule_deploy.html',locals())


@login_required()
def JobList(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        return render(request,'saltadmin/saltjob_list.html',locals())


@login_required()
def RemoteCmd(request):
    usersession = request.session.get('user_id')
    if request.method == 'GET':
        return render(request,'saltadmin/salt_cmd.html',locals())


