#!/usr/bin/env python
class people:
	name = ''
	age = 0
	__weight = 0
	def __init__(self,n,a,w):
		self.name = n
		self.age = a
		self.__weight = w
	def speak(self):
		print("i'm %s,%d years old,my weight is %d" %(self.name,self.age,self.__weight))

p = people('tom',30,70)
p.speak()
