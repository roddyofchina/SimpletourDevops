#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from django import forms
from servermanager.models import Server
from dockermanager.models import DockerHost
from django.forms import ModelForm









class DockerServerAdd(forms.Form):
    DockerServer=forms.ModelChoiceField(required=True,
                                        error_messages={'required': u'选择主机'},
                                        queryset=Server.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    ServerStatus = forms.ChoiceField(choices=[(0,u'禁用'),(1,u'启用')],widget=forms.Select(attrs={'class':'form-control'}))

    dockerip = forms.GenericIPAddressField(required=True,
                                           error_messages={'required': u'请输入dockerhost ip', 'invalid':u'ip地址错误'},
                                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '宿主机IP',
                                                               }),)
    dockerport = forms.IntegerField(required=True,
                                    error_messages={'required': u'请输入dockerhost port', 'invalid':u'port输入错误'},
                                    widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '宿主机端口',
                                    }),)

class DockerServerEdit(ModelForm):
    class Meta:
        model = DockerHost
        fields = ('host', 'hostip','port','enabled')
