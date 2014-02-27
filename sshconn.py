#!/usr/bin/env python

from multiprocessing import Process
import datetime
import time
import os

commands = ['step1_stop','step2_update','step3_start']
commands.sort()
def prtime():
	time.sleep(19)
	now = str(datetime.datetime.now())
	#print 'finally pid is %s & parent is %s ' % (os.getpid(),os.getppid())
	print '\t'+now +' '+ com

def subid(b):
	s = []
	for p in xrange(4):
		s.append(Process(target=prtime))
		s[p].start()
	for t in s:
		t.join()

for com in commands:
	a = []
	for b in xrange(2):
		a.append(Process(target=subid,args=(str(b))))
		a[b].start()
	for y in a:
		y.join()

