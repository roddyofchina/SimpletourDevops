#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from servermanager.models import *
from webapp.models import *
from webapp.Extends import PageList
from webapp.tasks import SaltGrains,UpdateServerInfo
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

import json

@login_required()
def HostLists(request):
    return render(request,'servermanager/hosts.html')

@login_required()
@permission_required('servermanager.cmdb_assets_view',raise_exception=True)
def AssetsLists(request,page):
    usersession=request.session.get('user_id')
    if request.method == 'POST':
        searchdata = request.POST.get('search')
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Assets.objects.filter(Q(host_name__contains=searchdata) | Q(device_number__contains=searchdata)).count()
        result = Assets.objects.filter(Q(host_name__contains=searchdata) | Q(device_number__contains=searchdata)).order_by('-id')[start:end]
        url = "/server/assets"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)
        ret = {'Assetsdata': result,
                   'count': count,
                   'page': page,
                   'usersession':usersession}
        return render(request,'servermanager/assets_list.html', ret)
    else:
        AssetsData=Assets.objects.all()
        for asset in AssetsData:
            if Server.objects.filter(Assets=asset):

                asset.status = 1
                asset.save()
            else:
                asset.status = 2
                asset.save()
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Assets.objects.all().count()
        result = Assets.objects.all().order_by('-id')[start:end]
        url = "/server/assets"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)

        ret = {'Assetsdata': result,
                   'count': count,
                   'page': page,
                   'usersession':usersession}
        return render(request,'servermanager/assets_list.html', ret)

@login_required()
def AssetsDetail(request,id):
    usersession=request.session.get('user_id')
    if request.method == 'GET':
        result = Assets.objects.get(id=id)
        ret={'Assetsdata':result,'usersession':usersession}
        return render(request,'servermanager/assetsdetail.html',ret)

@login_required()
@permission_required('servermanager.cmdb_server_view',raise_exception=True)
def ServerList(request,page):
    usersession=request.session.get('user_id')
    if request.method  == 'POST':
        searchdata = request.POST.get('search')
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Server.objects.filter(Q(Assets__host_name__contains=searchdata) | Q(hostname__contains=searchdata) | Q(sn__contains=searchdata)).count()

        result = Server.objects.filter(Q(Assets__host_name__contains=searchdata) | Q(hostname__contains=searchdata) | Q(sn__contains=searchdata)).order_by('-id')[start:end]
        url = "/server/servers"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)
        ret = {'Serverdata': result,
                   'count': count,
                   'page': page,
                   'usersession':usersession}
        return render(request,'servermanager/servers_list.html', ret)
    else:
        #分页代码
        (page,start,end,per_item)=PageList.PageCount(page)
        count = Server.objects.all().count()
        result = Server.objects.all().order_by('-id')[start:end]
        url = "/server/servers"
        if count%per_item == 0:
            all_pages_count = count/per_item
        else:
            all_pages_count = count/per_item+1
        page=PageList.Page(page, url, all_pages_count)
        ret = {'Serverdata': result,
               'count': count,
               'page': page,
               'usersession':usersession}
        return render(request, 'servermanager/servers_list.html', ret)

@login_required()
def ServerDetail(request,id):
    usersession=request.session.get('user_id')
    if request.method == 'GET':
        ServerData = Server.objects.get(id=id)


        Diskall=ServerData.disk.all()
        colors = ["#5fbeaa","#ebeff2","#36404a","#5fbeaa","#ebeff2","#5d9cec"]

        Diskhtml=[]
        for i in range(Diskall.count()):
            disk={}
            disk['label']=Diskall[i].name.encode()   #传给前端去掉unicode
            disk['value']=Diskall[i].capacity.encode()
            disk['color']=colors[i]
            disk['highlight']=colors[i]
            Diskhtml.append(disk)

        ret = {'usersession':usersession,'ServerData':ServerData,'Diskhtml':json.dumps(Diskhtml)}
        return render(request,'servermanager/servers_detail.html',ret)

@login_required()
@permission_required('servermanager.delete_assets',raise_exception=True)
def DeleteServer(request,id):
    username = request.session.get('user_name')
    if request.method == 'GET':
        ServerData = Server.objects.get(id=id)
        ServerData.delete()

        msg=u'删除服务器信息 %s'  %ServerData.hostname
        Operation.objects.create(Opuser=username,Opaction=msg)
        return HttpResponse(u'删除主机成功')

@login_required()
@permission_required('servermanager.delete_assets',raise_exception=True)
def DeleteAsset(request,id):
    username = request.session.get('user_name')
    if request.method == 'GET':
        selectid=Assets.objects.filter(id=id)
        if Server.objects.filter(Assets=selectid):
            msg={'msgerror':u'请删除所关联的服务器!!'}
            return HttpResponse(json.dumps(msg))
        else:
            AssetData = Assets.objects.get(id=id)
            AssetData.delete()
            msg=u'删除资产信息 %s'  %AssetData.host_name
            Operation.objects.create(Opuser=username,Opaction=msg)
            msg={'msginfo':u'OK，资产信息删除成功!!!!'}
            return HttpResponse(json.dumps(msg))

@login_required()
@permission_required('servermanager.change_assets',raise_exception=True)
def ChangeAsset(request,id):
    usersession=request.session.get('user_id')
    username = request.session.get('user_name')
    if request.method == 'POST':
        PostData=request.POST
        AssetDsata=Assets.objects.get(id=id)
        AssetDsata.status = PostData['status']
        AssetDsata.Warranty =PostData['Warranty']
        AssetDsata.device_number = PostData['device_number']

        device_type=DeviceType.objects.get(id=PostData['device_type'])
        AssetDsata.device_type = device_type
        AssetDsata.host_name = PostData['host_name']

        idc = IDC.objects.get(id=PostData['idc'])
        AssetDsata.IDC = idc

        business = Business.objects.get(id=PostData['business'])
        AssetDsata.business = business
        AssetDsata.buy_time = PostData['buytime']
        AssetDsata.price = PostData['price']

        admin  = Suser.objects.get(id=PostData['admin'])
        AssetDsata.admin = admin
        AssetDsata.suse_time = PostData['start']
        AssetDsata.euse_time = PostData['end']

        provider = Provider.objects.get(id=PostData['provider'])
        AssetDsata.provider = provider

        AssetDsata.description = PostData['summernote']
        AssetDsata.save()


        Operation.objects.create(Opuser=username,Opaction=u'修改资产信息')

        msg={'msginfo':u'恭喜您，资产修改成功！！！'}
        return HttpResponse(json.dumps(msg))

    else:
        AssetsData=Assets.objects.get(id=id)
        IdcData = IDC.objects.all()
        BusinessData = Business.objects.all()
        DeviceTypeData  = DeviceType.objects.all()
        AdminUser = Suser.objects.all()
        ProviderData = Provider.objects.all()

        ret = {
            'usersession': usersession,
            'AssetsData': AssetsData,
            'IdcData': IdcData,
            'BusinessData': BusinessData,
            'DeviceTypeData': DeviceTypeData,
            'AdminUser': AdminUser,
            'ProviderData':ProviderData,
        }
        return render(request,'servermanager/assetschange.html',ret)


@login_required()
@permission_required('servermanager.change_server',raise_exception=True)
def ChangeServer(request,id):
    usersession=request.session.get('user_id')
    username = request.session.get('user_name')
    if request.method == 'POST':
        software=request.POST.getlist('software')
        disk=request.POST.getlist('disk')
        nic=request.POST.getlist('nic')

        Assetsid=request.POST['Assets']
        AssetsInfo = Assets.objects.get(id=Assetsid)

        ServerData=Server.objects.get(id=id)
        ServerData.Assets=AssetsInfo
        ServerData.mem = request.POST['mem']
        ServerData.swap=request.POST['swap']
        ServerData.platform = request.POST['platform']
        ServerData.system = request.POST['system']
        ServerData.version = request.POST['version']
        ServerData.Firm = request.POST['firm']
        ServerData.saltid = request.POST['saltid']
        ServerData.hostname = request.POST['hostname']
        ServerData.sn = request.POST['sn']
        CPU = request.POST['CPU']
        CPU = Cpu.objects.get(id=CPU)
        ServerData.cpu=CPU
        ServerData.cpu_count = request.POST['cpu_count']
        ServerData.cpu_core_count = request.POST['cpu_core_count']
        ServerData.raid = request.POST['raid']
        ServerData.addtype = request.POST['addtype']

        for n in ServerData.nic.all():
            group_set = NIC.objects.get(id=n.id)
            ServerData.nic.remove(group_set)

        for d in ServerData.disk.all():
            group_set = Disk.objects.get(id=d.id)
            ServerData.disk.remove(group_set)

        for s in ServerData.software.all():
            group_set = Software.objects.get(id=s.id)
            ServerData.software.remove(group_set)

        for n in nic:
            print n
            group_set = NIC.objects.get(id=n)
            ServerData.nic.add(group_set)

        for d in disk:
            group_set = Disk.objects.get(id=d)
            ServerData.disk.add(group_set)

        for s in software:
            group_set = Software.objects.get(id=s)
            ServerData.software.add(group_set)

        ServerData.save()
        Operation.objects.create(Opuser=username,Opaction=u'修改服务器信息')
        return HttpResponse(u'Server 修改成功!!')


    else:

        listdata=[]
        [listdata.append(int(i.Assets.id)) for i in Server.objects.all()]
        hostid=Server.objects.get(id=id)
        listdata.remove(hostid.Assets_id)
        AssetsData=Assets.objects.exclude(id__in=listdata)


        CpuData = Cpu.objects.all()
        SoftwareData = Software.objects.all()
        DiskData = Disk.objects.all()
        NicData = NIC.objects.all()
        ServerData = Server.objects.get(id=id)
        ret={'usersession':usersession,
             'AssetsData':AssetsData,
             'ServerData':ServerData,
             'SoftwareData':SoftwareData,
             'DiskData':DiskData,
             'NicData':NicData,
             'CpuData':CpuData}
        return render(request,'servermanager/servers_change.html',ret)


@login_required()
def UpdateServer(request,id):
    username = request.session.get('user_name')
    if request.method == 'GET':
        a=UpdateServerInfo.apply_async((str(id),))
        msg={'celeryId':a.id}
        Operation.objects.create(Opuser=username,Opaction=u'Salt更新服务器信息 服务器 %s' %id)
        return HttpResponse(json.dumps(msg))

@login_required()
def CeleryStatus(request,celeryid):
    if request.method == 'GET':
        task=UpdateServerInfo.AsyncResult(celeryid)
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






