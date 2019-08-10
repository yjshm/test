#!endcoding = utf-8  python3.7
import urllib
from urllib import request
import lxml
import lxml.etree
import platform


def downloadl(addr,mytype):
    url='https://search.51job.com/list/190300%252C190200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    req = request.Request(url=url,headers=headers)
    data = request.urlopen(req).read()
    mytree = lxml.etree.HTML(data)
    print(mytree.xpath('//*[@id="resultList"]/div[2]/div[4]/text()'))

downloadl('https://sou.zhaopin.com/?jl=749&sf=0&st=0&kw=python&kt=3',1 )
print ('Python', platform.python_version())
