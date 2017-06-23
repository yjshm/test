#coding:utf-8
#!/usr/bin/python


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def total(initial=5,*numbers,**keywords):
	'''
	total 有来演示函数的多参调用
	'''
	count = initial
	for number in numbers:
		count+=number
		print(u'number:%d'%number)
		
	for key in keywords:
		print(key) 
		print(keywords[key])
		count +=keywords[key]
	return count
	
# print(total(10,1,2,3,tableKey=50,fruits=100))
# print(u'%s'%total.__doc__)
# print(u'有来演示函数的多参调用')

#this is my shopping list 
shopplist =['apple','mango','carrot','bannan']
print (len(shopplist))
print ('it this are ',shopplist)

for item in shopplist:
	print(item)
	
shopplist.append('rice')
shopplist.sort()

del shopplist[0]
print shopplist