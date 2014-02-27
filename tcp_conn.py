#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os, sys, socket, time
from multiprocessing import Process


addr = '192.168.3.160'
port = 7901

def conn(addr,port):
    soc = socket.socket()
    soc.connect((addr,port))
    #soc.send('abcd')
    time.sleep(300)

for i in xrange(1500):
    p = Process(target=conn,args=(addr,port))
    p.start()
