#coding=utf-8
#5.6

import pdb
import sys
import time
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re

base_URL = 'http://m.baidu.com'
URL = 'http://m.baidu.com/s?wd='

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
#		pattern = re.compile('<div.*?c-container.*? id="(.*?)".*?data-click=.*?href(.*?)target' +\
#			'+.*?>(.*?)</a>',re.S)
		pattern = re.compile('<div.*?new_srcid="(.*?)".*?c-container.*?href=(.*?) class.*?>(.*?)</a>',re.S)			
#<div class="c-container"><a href="http://m.baidu.com/from=0/bd_page_type=1/ssid=0/uid=0/pu=usm%401%2Csz%40224_220%2Cta%40iphone___3_537/baiduid=FB84A26F7ACA56206410FAE3860F499E/w=20_10_/t=iphone/l=3/tc?ref=www_iphone&amp;lid=12753832614913792750&amp;order=7&amp;fm=alop&amp;tj=www_normal_7_20_10_title&amp;vit=osres&amp;m=8&amp;srd=1&amp;cltj=cloud_title&amp;asres=1&amp;title=...%E7%89%9B%E7%89%9B%E6%A3%8B%E7%89%8C%E6%B8%B8%E6%88%8F%E6%89%8B%E6%9C%BA%E7%89%88%E4%B8%8B%E8%BD%BD%E5%B0%8F%E6%B8%B8%E6%88%8F%2C2144%E5%B0%8F%E6%B8%B8%E6%88%8F...&amp;dict=32&amp;w_qd=IlPT2AEptyoA_ykz6BgbwwxsOUYwtYl3ZpJsnaax7K&amp;sec=21937&amp;di=c2361ad40ba06cdc&amp;bdenc=1&amp;nsrc=IlPT2AEptyoA_yixCFOxXnANedT62v3IEQGG_8wJRmr5nkryqRLeEcJjYTvq0S4FSpWcbDHOtQoDla" class="c-blocka">
#<h3 class="c-title c-gap-top-small">...<em>牛牛棋牌游戏</em>手机版下载<em>小游戏</em>,2144<em>小游戏</em>...</h3></a>
		items = re.findall(pattern,self.curContent)
		#pdb.set_trace()
		return items

	#下面两个函数是为了得到当前所处的页数
	def getPageContent(self,webcontent):
		'''
		这里已经将所有的关于该页搜索结果中的页码信息都得到
		可以在这里将其他页码的链接得到
		'''
		#pattern = re.compile('<div id="page" >(.*?)</div>',re.S)
		pattern = re.compile('<div class="new-pagenav c-flexbox">(.*?)</div>',re.S)
		
		pageContent = re.findall(pattern,webcontent)
		# print pageContent
		pageContent = pageContent[0]
		return pageContent
	def getCurrentPage(self):
		curPage = 0
		pageContent = self.getPageContent(self.curContent)
		#regx = r'<span class="pc">(\d)</span></strong>'
		regx = r'<span class="new-nowpage">.*?(第&nbsp;(\d)&nbsp;页)</span>'
		pm = re.search(regx,pageContent)
		if pm :
			curPage = pm.group(1)
		return curPage
	def getNextPage(self):
		nextPage = None
		pageContent = self.getPageContent(self.curContent)
		#regx = r'<span class="pc">(\d)</span></strong>'
		#regx = r'<span class="new-nowpage">(.*?)(第&nbsp;\d&nbsp;页)</span>'
		#第一页中的下一页
		regx = r'<a class="new-nextpage-only" href="(.*?)">.*?</a>'
		pm = re.search(regx,pageContent)
		if pm :
			nextPage = pm.group(1)
			print nextPage
		return nextPage
	
	def getHrefByPage(self,page):
		if page == self.getCurrentPage():
			print "It's the page you want"
			return
		print (u"current page is %d"%page)
		pageContent = self.getPageContent(self.curContent)
		#regx = re.compile(r'<a href="(.*?)">.*?<span class="pc">(\d)</span></a>',re.S)
			
		if page==1 :
			regx = re.compile(r'<a class="new-nextpage-only" href="(.*?)">.*?</a>',re.S)
		else :
			regx = re.compile(r'<a class="new-nextpage" href="(.*?)">.*?</a>',re.S)
		
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
		#baidu.nextpage = baidu.getHrefByPage(int(baidu.getCurrentPage())+1)
		baidu.nextpage = baidu.getNextPage()
		print(u'nextpage: %s'% baidu.nextpage)
		
		items = baidu.getHref()
			#打印出来
		print u'正在爬取第1页...'
		for item in items:
			#pdb.set_trace()
			strtemp = item[1].split('"')[1]
			#pFile.write(item[0]+','+strtemp+','+item[2])
					#pFile.write(item[0]+'\n')
					
			pFile.write(item[2]+'\n')
			pFile.write(strtemp+'\n')
			#pFile.write('\n')

		for i in range(5):
			print u'正在爬取第'+str(i+2)+'页...'
			baidu.getContent(baidu.nextpage)
			items = baidu.getHref()
			#打印出来
			for item in items:
				strtemp = item[1].split('"')[1]#网址
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


		
		





