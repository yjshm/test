#!endcoding = utf-8  python2.7
import  urllib2
import urllib
import lxml
import lxml.etree
import platform

def downloadl(addr,mytype):
    url='http://www.baidu.com'
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    request = urllib2.Request(url=url,headers=headers )
    data = urllib2.urlopen(request).read()
    mytree = lxml.etree.HTML(data)
    print(mytree.xpath('//*/div'))

downloadl('https://sou.zhaopin.com/?jl=749&sf=0&st=0&kw=python&kt=3',1 )
print ('Python', platform.python_version())
