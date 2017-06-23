#coding= utf-8
#!/urs/bin/python

import sys
import pickle

reload(sys)
sys.setdefaultencoding('utf-8')


class preson:
	count  = 0
	def __init__(self,name,birthday,tel,emaill):
		self.name = name
		self.birthday = birthday
		self.tel = tel 
		self.emaill = emaill
		preson.count +=1
		
	def __del__(self):
		preson.count -=1
	def __str__(self):
		str ='name:{0}  birthday:{1} tel:{2} emaill:{3}\n'.format(self.name,self.birthday,self.tel,self.emaill)
		#print str 
		return str 		
	


class addressList():
	fileName ="addressList.dat"
	def __init__(self):
		self.list =[]
		
	def addItem(self,preson):
	     self.list.append(preson)
		 
	def addItem(self,name,birthday,tel,emaill):
			temp =preson(name,birthday,tel,emaill)
			self.addItem(temp)
			
	def addItem(self):
			name = raw_input(u'input name:')
			birthday=raw_input(u'input birthday:')
			tel = raw_input (u'input tel:')
			emaill = raw_input (u'input emaill:')
			temp =preson(name,birthday,tel,emaill)
			self.list.append(temp)
			#self.addItem(self,name,birthday,tel,emaill)
		 
	def findItem(self,key):
		for item in self.list:
		   if item.name == key or item.birthday==key or item.emaill==key or item.tel==key :
				print (u'find the key',item)
				return item
		     
	
	def delItem(self,key):
		i =0
		while i < len(self.list):
			item = self.list[i]
			if item.name == key or item.birthday==key or item.emaill==key or item.tel==key :
				print (u'find the key:',self.list[i])
				del(self.list[i])
				return 
			i+=1	
		   
	def loadList(self):
		f = open(addressList.fileName)
		if f :
			self.list = pickle.load(f)
			f.close()
			print(u'load list from file:',self.list)
	
	def saveList(self):
	   f =open(addressList.fileName,'wb')
	   self.list.sort()
	   pickle.dump(self.list,f)
	   f.close()
	   print(u'save list to file:',self.list)
	
	def dump(self):
		for item in self.list:
		 print item ;
	
	
myaddress = addressList()
myaddress.loadList()
myaddress.dump()

while True:
	print'---------------------'
	print'--add:{0} find:{1} del:{2} show:{3} save:{4} quit:{5}-------------------'.format('add','find','del','show','save','quit')
	process = raw_input("input process:")
	if process =='add': 	#add presson
		myaddress.addItem()
	elif process=='find':
		key = raw_input("input you find key:")
		print  myaddress.findItem(key)
	elif process=='del':
		key = raw_input("input you del key:")
		print  myaddress.findItem(key)
		myaddress.delItem(key)
	elif process=='show':
		myaddress.dump()
	elif process=='save':
		myaddress.saveList()
	else: #'quit':
		break
