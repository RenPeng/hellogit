#!/usr/bin/env python
# -*- coding=utf-8 -*-

def pprint(contant):
    print contant.a
    print contant.b

class callself(object):
    def __init__(self):
        self.a = 'asdf'
        self.b = 'a method'
        #pprint(self)
    def amethod(self):
        pprint(self)

a = callself()
a.amethod()
