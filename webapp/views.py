#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from webapp.models import Suser, History_Login,Operation
from webapp import forms
from webapp.tasks import sendmail,resetpass
from django.conf import settings as django_settings
from itsdangerous import TimestampSigner
from django.db.models import Sum
from servermanager.models import *
from dockermanager.models import *
import json


@login_required
def index(request):
    priceData = Assets.objects.all().aggregate(Sum('price'))
    #如果用户从管理后台登录将设置session值
    if not request.session.get('user_id'):
        usersession = request.session.get('_auth_user_id')
        request.session['user_id'] = usersession
    else:
        usersession = request.session.get('user_id')
    ServersCount = Server.objects.all().count()
    DockerContainerCount = DockerContainer.objects.all().count()
    DockerImageCount = Dockerimage.objects.all().count()
    UserData = Suser.objects.get(id=usersession)
    Opdata = Operation.objects.all().order_by('-id')[:10]
    return render(request,'webapp/index.html',locals())

#用户登录函数
def Login(request):
    restdata = {'data':'', 'error': ''}
    loginobj=forms.SimpleLogin()
    restdata['data'] = loginobj
    if request.method == 'POST':
        CheckForm = forms.SimpleLogin(request.POST)
        if CheckForm.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            #设置用户的会话过期时间,如果没有勾记住我，默认关闭浏览器就要重新登录
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    request.session['user_name'] = user.username
                    request.session['user_id'] = user.id
                    #记录用户登录日志
                    history_login = History_Login(
                         user=user,
                         user_ip=request.META['REMOTE_ADDR'],
                         request_method=request.META['REQUEST_METHOD'],
                         request_url=request.META['HTTP_REFERER'],
                    )
                    history_login.save()
                    msg={'msginfo':'login is ok'}
                    return HttpResponse(json.dumps(msg))
                else:
                    msg={'msgerror':u"用户没有激活!!!"}
                    return HttpResponse(json.dumps(msg))
            else:
                msg={'msgerror':u"用户名或密码错误"}
                return HttpResponse(json.dumps(msg))
        else:
            restdata['data'] = CheckForm
            restdata['error'] = CheckForm.errors.as_data().values()[0][0].messages[0]
    return render(request, 'webapp/login.html', restdata)

#用户注册函数
def Register(request):
    restdata = {'data':'','regerror':''}
    registerobj=forms.Register()       #实例化forms
    restdata['data'] = registerobj     #将对象传到模板中

    if request.method == 'POST':
        form = forms.Register(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if not Suser.objects.all().filter(email=email):    #先判断是否存在该用户
                if form.pwd_validate(password1,password2):     #判断密码是否一致
                    user = Suser.objects.create_user(email,username,password1)
                    user.save()
                    #生成验证连接并发送邮件
                    s=TimestampSigner(django_settings.SECRET_KEY)
                    registerstring = s.sign(email)
                    sendmail.delay(dict(to=email,string=registerstring))   #发送邮件
                    return HttpResponseRedirect('/web/login/')
                else:
                    error=u'密码输入不一致!!'
                    restdata['regerror'] = error
            else:
                error=u'用户已存在，请重新输入!!!!!'
                restdata['regerror'] = error
        else:
            restdata['data'] = form
    return render(request,'webapp/register.html',restdata)

#激活用户函数
def Activate(request, token):
    s=TimestampSigner(django_settings.SECRET_KEY)
    email=s.unsign(token)
    try:
        s=TimestampSigner(django_settings.SECRET_KEY)
        s.unsign(token,max_age=300)
    except:
        users=Suser.objects.filter(email=email)
        for user in users:
            user.delete()
        return HttpResponse('连接已过期!!')

    try:
        user = Suser.objects.get(email=email)
    except Suser.DoesNotExist:
        return HttpResponse('用户不存在!!')

    user.is_active=True
    user.save()
    return HttpResponseRedirect('/')

#用户退出
def Logout(request):
    #记录用户登出时间
    #history_login = History_Login.objects.filter(user=request.user).order_by('-id')[0]
    #history_login.save()
    #登出用户
    logout(request)
    #删除用户的session
    if request.session.get('user_name'):
        del request.session['user_name']
    return HttpResponseRedirect('/',)


#发送重置密码链接给用户
def SendResetEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Suser.objects.get(email=email)
        except Suser.DoesNotExist:
            msg={'msgerror':u'对不起，您输入的用户不存在,请重新输入!!!'}
            return HttpResponse(json.dumps(msg))

        s=TimestampSigner(django_settings.SECRET_KEY)
        resetstring = s.sign(email)
        resetpass.delay(dict(to=email,string=resetstring))
        msg={'msginfo':u'邮件发送成功,请及时确认!!!!'}
        return HttpResponse(json.dumps(msg))
    else:
        return render(request,'webapp/sendresetpw.html')


#重置密码
def ResetPassword(request,token):
    restdata = {'data':'','regerror':'','token':token}
    registerobj=forms.Register()
    restdata['data'] = registerobj
    if request.method == 'POST':
        s=TimestampSigner(django_settings.SECRET_KEY)
        email=s.unsign(token)

        form = forms.ResetPassword(request.POST)
        if form.is_valid():
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if form.pwd_validate(password1,password2):
                try:
                    s=TimestampSigner(django_settings.SECRET_KEY)
                    s.unsign(token,max_age=300)
                except:
                    msg={'msgerror':u'哎哟我去，连接已过期,请重发邮件!!'}
                    return HttpResponse(json.dumps(msg))
                users=Suser.objects.get(email=email)
                users.set_password(password1)
                users.save()
                msg={'msginfo':u'恭喜您，密码修改成功!!!'}
                return HttpResponse(json.dumps(msg))
            else:
                msg={'msgerror':u'密码输入不一致!!'}
                return HttpResponse(msg)
        else:
            restdata['data'] = form
    else:
        return render(request,'webapp/resetpass.html', restdata)


#个人信息
@login_required()
def Userinfo(reqest):
    userid = reqest.session.get('user_id')
    if reqest.method == 'GET':
        Userdata=Suser.objects.get(id=userid)
        data={'Userdata':Userdata,'usersession':reqest.session.get('user_id')}
        return render(reqest,'webapp/userinfo.html',data)


@login_required()
def SysrestUserpassword(request,id):
    restdata = {'data':'','regerror':'','id':int(id),'usersession': request.session.get('user_id')}
    registerobj=forms.Register()
    restdata['data'] = registerobj
    if request.method == 'POST':
        form = forms.ResetPassword(request.POST)
        if form.is_valid():
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if form.pwd_validate(password1,password2):
                users=Suser.objects.get(id=id)
                users.set_password(password1)
                users.save()
                return HttpResponse('密码修改成功')
            else:
                error=u'密码输入不一致!!'
                return HttpResponse(error)
        else:
            restdata['data'] = form
    else:
        return render(request,'webapp/sysrestuserpassword.html', restdata)



