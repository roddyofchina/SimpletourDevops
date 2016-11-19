#coding:utf8
from django.contrib import admin
from django.contrib.admin import models
from django import forms
from webapp.models import *
from django.forms import ModelForm,TextInput,Textarea
from django.contrib.auth.admin import UserAdmin  # 从django继承
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单

admin.AdminSite.site_header ='管理系统后台'
admin.AdminSite.site_title = '运维后台'




#以下代码曲东同学分享，博客地址http://www.cnblogs.com/caseast/p/5909987.html
class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True

class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True



class CustomUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CustomUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'name', 'email', 'is_staff', 'is_superuser','phone')
        self.search_fields = ('username', 'email', 'name')
        self.form = MyUserChangeForm
        self.add_form = MyUserCreationForm


    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                              (('Personal info'), {'fields': ('name', 'email','phone')}),
                              (('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
                              (('Important dates'), {'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
                                                     'is_staff', 'groups','phone'),
                                          }),
                                  )
        else:
            self.fieldsets = (((u'登录信息'), {'fields': ('username', 'password',)}),
                              ((u'用户信息'), {'fields': ('name', 'email', 'phone')}),
                              ((u'用户权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                              ((u'加入时间'), {'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'name', 'password1', 'password2', 'email', 'phone','QQ', 'age','department', 'is_active',
                                                     'is_staff', 'is_superuser', 'groups',),
                                          }),
                                  )

        return super(CustomUserAdmin, self).changelist_view(request, extra_context)



# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','phone', 'email','department','is_staff',  'is_superuser')
    search_fields = ('name','email','username')
    list_filter = ('department','is_active','groups')


class LoginHistory(admin.ModelAdmin):
    list_display = ('user','user_ip','login_time','logout_time','request_method','request_url')


#admin.site.register(Suser,CustomUserAdmin)
admin.site.register(Suser,CustomUserAdmin)
admin.site.register(Department)
admin.site.register(History_Login,LoginHistory)



