#coding=utf-8
#5.6


import sys
import time
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re

base_URL = 'http://www.baidu.com'
URL = 'http://www.baidu.com/s?wd='

class Baidu():
	session = requests.Session()
	#这个变量存储当前页的网页代码
	curContent = ''
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'+\
	 '(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	nextpage = ''
	def getContent(self,url):
		r = self.session.get(url,headers = self.headers)
		self.curContent = r.content
	def getHref(self):
		pattern = re.compile('<div.*?c-container.*? id="(.*?)".*?data-click=.*?href(.*?)target' +\
			'+.*?>(.*?)</a>',re.S)
		items = re.findall(pattern,self.curContent)
		return items

	#下面两个函数是为了得到当前所处的页数
	def getPageContent(self,webcontent):
		'''
		这里已经将所有的关于该页搜索结果中的页码信息都得到
		可以在这里将其他页码的链接得到
		'''
		pattern = re.compile('<div id="page" >(.*?)</div>',re.S)
		pageContent = re.findall(pattern,webcontent)
		# print pageContent
		pageContent = pageContent[0]
		return pageContent
	def getCurrentPage(self):
		pageContent = self.getPageContent(self.curContent)
		regx = r'<span class="pc">(\d)</span></strong>'
		pm = re.search(regx,pageContent)
		curPage = pm.group(1)
		return curPage
	def getHrefByPage(self,page):
		if page == self.getCurrentPage():
			print "It's the page you want"
			return
		pageContent = self.getPageContent(self.curContent)
		regx = re.compile(r'<a href="(.*?)">.*?<span class="pc">(\d)</span></a>',re.S)
		pm = re.findall(regx,pageContent)
		for item in pm:
			if int(item[1]) == page:
				return item[0]
	def getTrueUrl(self,findBaidu,trueUrl):
    #def getTrueUrl(self,findBaidu):
		#trueUrl = u'./真实URL.txt'
		filterFile = u'./过滤.txt'
		
		print (findBaidu)
		pFile = open(findBaidu,'r')
		pFileOut = open(trueUrl,'w')
		pFileFilter = open(filterFile,'r')
		  
		arrayUrl = []
		arrayFilter = []
		#读取过滤文件
		buff = u'过滤字符'
		for line in pFileFilter.readlines():
			buff = (line.strip().decode('utf-8', 'ignore'))
			arrayFilter.append(buff)
			print (u"过滤字符 :%s \n" % buff)
		pFileFilter.close()
		
		
		count = 0;
		for line in pFile.readlines():
			url = line.strip().decode('utf-8', 'ignore')
			#print url 
			regx =r'http'
			pm = re.search(regx,url)
			if pm :
				arrayUrl.append(url.rstrip()) #只保存url
			#if count %10 :
			#	time.sleep(10)  #休眠处理
		#arrayUrlSort = sorted(arrayUrl)
		#print(arrayUrlSort)
		
		for url in arrayUrl:
			try:
				#print url
				r = requests.get(url, timeout = 3)
				
				#清除包含过滤字符网址
				bFind = False
				for filterStr in arrayFilter:
					#print filterStr
					finded = re.search(filterStr,r.url)
					if finded :
						print (u'过滤此网址:...包含 %s' %filterStr)
						print r.url
						bFind = True
						break
						
				if not bFind :	
					print u'保存网址:...'
					print r.url
					pFileOut.write(r.url+'\n')
				#time.sleep(3) 
			except (RuntimeError, TypeError, NameError,requests.exceptions,requests.ConnectionError, requests.exceptions.RequestException ):
				pFileOut.flush();
				time.sleep(1) 
				pass
			
		pFileOut.close()
		pFile.close()	
		return 0


if __name__=='__main__':
	#可以使用一个列表建立将所有的关键词都加入进去
	#testword = [u'wc']
	testword = u'关键字'
	findway = u'./data/关键字.txt'#测试用例
	
	pKeyFile = open(u'关键字.txt','r')  
	for line in pKeyFile.readlines():
		#print(line.strip()) # 把末尾的'\n'删掉
		testword = line.strip().decode('utf-8', 'ignore')
		#testword = testword.decode('utf-8', 'ignore')
		
		#关键字删除中间空格生成文件名
		fileName= ''.join(testword.split())
		
		findway = u'./data/%s.txt'%(fileName)
		trueUrl = u'./解析结果/%s-URL.txt'%(fileName)
		print(findway)
		
		
		#如下得到该页内网页搜索十个结果的连接
		pFile = open(findway,'a+')
		pFile.write(testword+'\n')

		baidu = Baidu()
		#baidu.getTrueUrl(findway,trueUrl);
		#sys(exit)
		
		baidu.getContent(URL+testword)
		baidu.nextpage = baidu.getHrefByPage(int(baidu.getCurrentPage())+1)
		items = baidu.getHref()
			#打印出来
		print u'正在爬取第1页...'
		for item in items:
			strtemp = item[1].split('"')[1]
			#pFile.write(item[0]+','+strtemp+','+item[2])
					#pFile.write(item[0]+'\n')
					
			pFile.write(item[2]+'\n')
			pFile.write(strtemp+'\n')
			#pFile.write('\n')

		for i in range(75):
			print u'正在爬取第'+str(i+2)+'页...'
			baidu.getContent(base_URL+baidu.nextpage)
			items = baidu.getHref()
			#打印出来
			for item in items:
				strtemp = item[1].split('"')[1]
				#pFile.write(item[0]+'\n')
				pFile.write(item[2]+'\n')#标题
				pFile.write(strtemp+'\n')
				#print strtemp

				#print '\n'
				#pFile.write(item[0]+','+strtemp+','+item[2])
				#pFile.write('\n')
			baidu.nextpage = baidu.nextpage.replace('pn=%s'%unicode((i+1)*10),'pn=%s'%unicode((i+2)*10))	
		
		
		pFile.close()
		print u'解析真实URL...'
		baidu.getTrueUrl(findway,trueUrl)		
	pKeyFile.close()
	print u'完成'	


		
		





