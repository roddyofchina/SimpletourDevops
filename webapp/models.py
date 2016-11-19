# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,Group,PermissionsMixin
from django.utils import six, timezone

class Department(models.Model):
    name = models.CharField(max_length=64, unique=True)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'部门管理'
        verbose_name_plural = u"部门管理"
        permissions = (
            ("webapp_dept_add", u"添加部门信息"),
            ("webapp_dept_view", u"查看部门信息"),
            ("webapp_dept_change", u"修改部门信息"),
            ("webapp_dept_delete", u"删除部门信息"),
        )

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class Suser(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(
        verbose_name=u'邮箱',
        max_length=255,
        unique=True,
    )

    username = models.CharField(max_length=50,verbose_name=u'用户名')

    is_active = models.BooleanField(default=True, verbose_name=u'激活用户',help_text=(
            '设置用户状态。'

        ),)

    is_staff = models.BooleanField(default=False,verbose_name=u'职员状态',help_text=(
            '是否设置用户可登录管理站点。'

        ),)


    #全名
    name = models.CharField(u'姓名',max_length=20, null=True)

    #电话号码
    phone = models.CharField(max_length=12,null=True,blank=True,verbose_name=u'联系方式')

    #部门
    department = models.ForeignKey('Department',null=True,blank=True,verbose_name=u'部门')

    #用户QQ信息
    QQ = models.CharField(max_length=50,null=True,blank=True)

    #年龄
    age = models.IntegerField(null=True,blank=True,verbose_name=u'年龄')

    date_joined = models.DateTimeField(verbose_name=u'创建时间', default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff


    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = u'用户管理'
        verbose_name_plural = u"用户管理"
        #unique_together = ('email', )

        permissions = (
            ("webapp_users_add", u"添加用户"),
            ("webapp_users_view", u"查看用户"),
            ("webapp_users_view_info", u"查看用户详细"),
            ("webapp_users_change", u"修改用户"),
            ("webapp_users_delete", u"删除用户"),
            ("webapp_users_restpass", u"修改用户密码"),
        )

class History_Login(models.Model):
    user = models.ForeignKey(Suser)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(auto_now=True)
    request_method = models.CharField(max_length=12, null=True)
    request_url = models.CharField(max_length=100, null=True)
    user_ip = models.GenericIPAddressField()

    class Meta:
        verbose_name = u'登录历史'
        verbose_name_plural = u"登录历史"
        permissions = (
            ("webapp_history_view", u"查看登录历史"),
            ("webapp_history_delete", u"删除登录历史"),
        )

class Operation(models.Model):
    Opuser = models.CharField(max_length=12, null=True)
    Optime = models.DateTimeField(auto_now_add=True)
    Opaction = models.CharField(max_length=50, null=True)
    class Meta:
        verbose_name = u'操作记录'
        verbose_name_plural = u'操作记录'



