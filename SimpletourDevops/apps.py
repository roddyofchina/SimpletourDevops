#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'

    menu = (

    )
