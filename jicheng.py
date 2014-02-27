#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os,sys

class a(object):
    def __init__(self,name):
        self.name = name
    def aa(self):
        self.age = '30'

class b(a):
    def __init__(self,name):
        a.__init__(self,name)
        self.name = 'tom'
    def b(self):
        self.aa()
        print 'i\'m %s,and %s yesrs old' %(self.name,self.age)

b = b('renpeng')
b.b()
