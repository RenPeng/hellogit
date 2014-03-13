#!/usr/bin/env python
# -*- coding=utf-8 -*-
choose1 = raw_input('需要转换的中文字符: ')
print ['gbk: '] + choose1.decode('utf-8').encode('gbk').split()
print ['utf8: '] + choose1.decode('utf-8').encode('utf-8').split()

