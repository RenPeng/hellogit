#!/usr/local/bin/python
# -*- coding=utf-8 -*-

import socket, time

s = socket.socket()
hostname = socket.gethostname()
port = 1122
s.bind(('192.168.6.168',port))
s.listen(500000000)
while True:
    c,addr = s.accept()
    print 'got connection from' , addr
    c.send('thank you for connecting')
    time.sleep(1000)
    c.close()

