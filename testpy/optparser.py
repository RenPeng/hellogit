#!/usr/bin/env python
# -*- coding=utf-8 -*-
import argparse,sys,os
parser = argparse.ArgumentParser(prog=sys.argv[0],description='some help',epilog='the end')
parser.add_argument('-f','--file',help='the filename',nargs=(1))
parser.add_argument('-p','--port',help='the port number',default=1024,type=int)
parser.add_argument('-F','--forward',help='the forward address')
a = parser.parse_args()
print a
if not a.file:
    sys.exit(parser.print_help())
if not os.path.exists(a.file[0]):
    print a.file[0]
    sys.exit('No Such file %s' % a.file[0])
