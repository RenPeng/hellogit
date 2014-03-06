#!/usr/bin/env python
# -*- coding=utf-8 -*-
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(parent_conn,))
    p.start()
    print child_conn.recv()   # prints "[42, None, 'hello']"
    p.join()
