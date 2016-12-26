#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'

    menu = (
        ParentItem(u'资产组件', children=[
            ChildItem(model='servermanager.server'),
            ChildItem(model='servermanager.assets'),
            ChildItem(model='servermanager.idc'),
            ChildItem(model='servermanager.cpu'),
            ChildItem(model='servermanager.nic'),
            ChildItem(model='servermanager.disk'),
            ChildItem(model='servermanager.software'),
            ChildItem(model='servermanager.business'),
            ChildItem(model='servermanager.devicetype'),
            ChildItem(model='servermanager.provider'),
        ], icon='fa fa-leaf'),

        ParentItem(u'容器管理', children=[
            ChildItem(model='dockermanager.dockerhost'),
            ChildItem(model='dockermanager.dockercontainer'),
            ChildItem(model='dockermanager.dockerimage'),
        ], icon='fa fa-magnet'),

        ParentItem(u'Salt管理', children=[
            ChildItem(model='saltadmin.saltjobs'),
            ChildItem(model='saltadmin.cmdrunlog'),
            ChildItem(model='saltadmin.miniongroup'),
            ChildItem(model='saltadmin.modules'),
        ], icon='fa fa-magnet'),

        ParentItem(u'用户管理', children=[
            ChildItem(u'用  户','webapp.suser'),
            ChildItem(u'用户组', 'auth.group'),
        ], icon='fa fa-users'),



    )
