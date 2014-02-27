#!/usr/bin/env python
# -*- coding=utf-8 -*-

name_dic = {}
name_dic['first'] = {}
name_dic['middle'] = {}
name_dic['last'] = {}
lables = ['first','middle','last']

def lookup(dic,key,name):
	return dic[key].get(name)


while True:
	full_name = raw_input('Input your full name: ')
	names = full_name.split()

	if len(names) == 2: names.insert(1,' ')

	for lable,name in zip(lables,names):
		people = lookup(name_dic,lable,name)
		if people:
			pass
		else:
			name_dic[lable][name] = names
			print name_dic
