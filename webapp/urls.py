from django.conf.urls import url
from webapp.views import (Login,
                          Logout,
                          Register,
                          Activate,
                          SendResetEmail,
                          ResetPassword,
                          SysrestUserpassword,
                          Userinfo)

urlpatterns = [
    url(r'login/$', Login, name='Login'),
    url(r'register/$', Register, name='Register'),
    url(r'logout/$', Logout, name='Logout'),
    url(r'activate/(?P<token>\w+@\w+.\w+.[-_\w]*\w+.[-_\w]*\w+)/$', Activate, name='Activate'),
    url(r'reset/$',SendResetEmail,name='SendResetEmail'),
    url(r'resetpass/(?P<token>\w+@\w+.\w+.[-_\w]*\w+.[-_\w]*\w+)/$', ResetPassword, name='ResetPassword'),
    url(r'userinfo/$',Userinfo, name='Userinfo'),
    url(r'restuserpass/(\d+)$', SysrestUserpassword, name='SysrestUserpassword'),
]
