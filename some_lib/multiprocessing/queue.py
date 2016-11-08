#!/usr/bin/env python
#-*- coding:utf-8 -*-

import Queue

import threading

import time

import random

q = Queue.Queue(0) #当有多个线程共享一个东西的时候就可以用它了

NUM_WORKERS = 3

class MyThread(threading.Thread):
	def __init__(self,input,worktype):
		self._jobq = input
		self._work_type = worktype
		threading.Thread.__init__(self)
def run(self):
	while True:
		if self._jobq.qsize() > 0:
			job = self._jobq.get()
			worktype = self._work_type
			self._process_job(job,worktype)
		else:break
def _process_job(self,job,worktype):
	doJob(job)
def doJob(job):
	time.sleep(random.random() * 3)
	print "doing",job

if __name__ == '__main__':
	print "begin ...."
	for i in range(NUM_WORKERS * 2):
		q.put(i) #放入到任务队列中去
		print "job q size:",q.qsize()
		for x in range(NUM_WORKERS):
			MyThread(q,x).start()
