#!/usr/bin/env python
# -*- coding=utf-8 -*-
from multiprocessing import Process, Lock
import time

def f(l, i):
    l.acquire()
    time.sleep(abs(i-10))
    print 'hello world', i
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()

