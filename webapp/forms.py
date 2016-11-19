#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from django import forms


class SimpleLogin(forms.Form):
    username = forms.EmailField(label='email',
                                error_messages={'required': u'请输入用户名', 'invalid':u'Email格式错误'},
                                widget=forms.EmailInput(attrs={'class': 'form-control',
                                                               'placeholder': '邮 箱',
                                                               }),
                                )
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': '密  码',
                                                                 }))

class Register(forms.Form):

    email = forms.EmailField(label='email',
                                error_messages={'required': u'请输入Email', 'invalid':u'Email格式错误'},
                                widget=forms.EmailInput(attrs={'class': 'form-control',
                                                               'placeholder': '邮 箱',
                                                               }),
                                )

    username = forms.CharField(label='username',
                                error_messages={'required': u'请输入用户名', 'invalid':u'用户名格式错误'},
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': '用户名',
                                                               }),
                                )

    password1 = forms.CharField(label='password1',
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': '密  码',
                                                                 }))

    password2 = forms.CharField(label='password2',
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': '再次输入密码',
                                                                 }))

    def pwd_validate(self,pwd1,pwd2):
        return pwd1==pwd2


class ResetPassword(forms.Form):


    password1 = forms.CharField(label='password1',
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': '密  码',
                                                                 }))

    password2 = forms.CharField(label='password2',
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': '再次输入密码',
                                                                 }))

    def pwd_validate(self,pwd1,pwd2):
        return pwd1==pwd2










