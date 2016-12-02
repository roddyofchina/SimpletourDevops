from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


@login_required()
def KeyList(request):
    if request.method == 'GET':

        pass
    return HttpResponse('OK')


@login_required()
def MinionStatus(request):
    if request.method == 'GET':
        pass
    return HttpResponse('OK')


@login_required()
def SoftInstall(request):
    if request.method == 'GET':
        pass
    return HttpResponse('OK')


@login_required()
def JobList(request):
    if request.method == 'GET':
        pass
    return HttpResponse('OK')


@login_required()
def RemoteCmd(request):
    if request.method == 'GET':
        pass
    return HttpResponse('Ok')


