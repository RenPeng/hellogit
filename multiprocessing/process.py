#!/usr/bin/env python
# -*- coding=utf-8 -*-
from multiprocessing import Process, Lock
import time, signal

def ff(i,l):
    print 'hello world', i
    time.sleep(3)

if __name__ == '__main__':
    namelist = ['renpeng','xuqiangqiang','liqian','wangshuai']
    for i in namelist:
        lock = Lock()
        pro = Process(target=ff,args=(i,lock))
        pro.start()
        pro.terminate()
        time.sleep(0.1)
        print pro , pro.is_alive()
        if pro.exitcode  == -signal.SIGTERM:
            print 'ok'
