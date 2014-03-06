#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
sep = os.sep
for root,dir,file in os.walk('/data/soft'):
	for i in file:
		a = (root+sep+i)
		print a
        print " on master"
        print "iss33"
