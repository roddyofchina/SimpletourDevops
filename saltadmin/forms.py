#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from django import forms
from saltadmin.models import SaltServer,Minions


class KeyManager(forms.Form):
    status = forms.ChoiceField(choices=Minions.Status,widget=forms.Select(attrs={'class':'form-control'}))



class CheckSaltServer(forms.ModelForm):
    url=forms.URLField(required=True,error_messages={'required': u'请输入一个URL格式'},
                       widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'http://127.0.0.1',}))

    username = forms.CharField(required=True,error_messages={'required':u'请输入API用户名'},
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'username',}))

    password = forms.CharField(required=True, error_messages={'required': u'请输入API验证密码'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password', }))


    # def clean(self):
    #     cleaned_data = sum(CheckSaltServer,self).clean()
    #     value = cleaned_data.get('url')
    #     try:
    #         SaltServer.objects.get(url=value)
    #         self._errors['url'] = self.error_class(["%s url 信息已存在" % value])
    #     except SaltServer.DoesNotExist:
    #         pass
    #     return cleaned_data


    class Meta:
        model = SaltServer
        exclude= ('id',)
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }





