#coding=utf-8
# 获取RSS

import re
import json
import io
import time
import requests
import xmltodict
import logging
from PIL import Image
from bs4 import BeautifulSoup


#import shutil
#import urllib3
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

class youporn():
    __feedlist= []
    __down_path = r'D:/work_GS/demo/img/'
    __resize_path = r'D:/work_GS/demo/reimg/'
    #添加头部，伪装浏览器，字典格式
    __headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
    img_url  =r'http://192.168.127.254:8080/infytb/img/'

    def __init__(self, feedlist):
        self.__feedlist = feedlist

    #下载图片并调整保存
    def down_img(self,url,save_name):
        file_name = url.split('/')[-1]
        try :
            #增加headers参数
            response = requests.get(url=url, headers=self.__headers)
            if not response :
                return False
            downfile = self.__down_path+file_name
            resizefile = self.__resize_path+save_name
            with open(downfile, 'wb') as f:
                f.write(response.content)
                logging.debug("{} ok".format(url))  
        except:
            print("error:{}".format(url))
            logging.warning(url)
        return self.resize_by_width(downfile,resizefile,120)

    #按照宽度进行所需比例缩放图片
    def resize_by_width(self,infile, outfile,w_divide_h):
        im = Image.open(infile)
        (x, y) = im.size 
        x_s = x
        y_s = x/w_divide_h
        #out = im.resize((x_s, y_s), Image.ANTIALIAS) 
        out = im.resize((120,90))
        out.save(outfile)
        logging.debug(outfile)
        return True

    #得到rss 数据并解析
    def get_rss(self,feedlist):
        rss = {}
        for url in feedlist:
            rss['rss'] = {
                'channel':
                {
                'title': '',
                'item': []
                }
            }
        #try:
            '''
            # 实例化一个启动参数对象
            chrome_options = Options()
            # 添加启动参数
            chrome_options.add_argument('--window-size=1366,768')
            # 将参数对象传入Chrome，则启动了一个设置了窗口大小的Chrome
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get(url)
            time.sleep(0.5)
            text = browser.page_source
            '''
            response = requests.get(url=url, headers=self.__headers)
            text = str(response.content, encoding='utf-8')
            logging.debug ('get_rss:',text) # 打印网页的内容
            
            soup = BeautifulSoup(text, 'lxml')
            title = soup.title.get_text()
            rss['rss']['channel']['title'] = title
            patterstr = r'<item>.*?' \
                     r'<title>(.*?)</title>.*?' \
                     r'<link>(.*?)</link>.*?' \
                     r'<description>(.*?)</description>.*?' \
                     r'<pubDate>(.*?)</pubDate>.*?' \
                     r'<guid>(.*?)</guid>.*?' \
                     r'</item>'
                     #r'<description>.*?<br>(.*?)<br.*?' \
            patterImgStr =r'img border=\"*?\" src=\"(*?)\"'
                     
            pattern = re.compile(patterstr,re.S)   #使用多行模式
            results = re.findall(pattern, text)   #如何查询多次

            if results!=None or len(results)==0:
                for result in results:
                    suburl = {
                        'title': result[0].replace(']]>', '').replace('<![CDATA[', ''),
                        'link': result[1].replace(']]>', '').replace('<![CDATA[', ''),
                        'description': result[2].replace(']]>', '').replace('<![CDATA[', ''),
                        'pubDate': result[3].replace(']]>', ''),
                        'guid': result[3],
                        'img' : "" 
                    }
                    #print('description',suburl['description'])
                    #patternImg = re.compile(patterImgStr,re.I)
                    #searchObj = re.search(r'', suburl['description'],re.I)
                    searchObj = re.search( r'img border=.* src=\"(.*?)\"', suburl['description'], re.I)
                    if searchObj :
                        suburl['img'] = searchObj.group(1)
                        print("img str",searchObj.group(1))
                        #return 
                    
                    #print(suburl)
                    rss['rss']['channel']['item'].append(suburl)
        #except:
        #    print("error: %s" % url)
        return rss


    def json2xml(self,js):
        convertXml=''
        json_data = ''
        with open(js,r"r+") as f:
            json_data = f.read() 

        jsDict=json.loads(json_data)
        #print(jsDict)
        try:
            convertXml=xmltodict.unparse(jsDict,encoding='utf-8')
            #print(convertXml)
        except:
            convertXml=xmltodict.unparse({'channel':jsDict},encoding='utf-8')
        finally:
            return convertXml


# 根据rss下载图片并调整尺寸
# 更改xml 地址重新生成rss
def main():
    logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
    feedlist=[
        'https://www.youporn.com/rss/'  
         ]
    downfile = ""
    m_youporn = youporn(feedlist)
    rss = m_youporn.get_rss(feedlist)

    if rss :
        file_id =1;
        for item in rss['rss']['channel']['item'] :
            downfile =  item['img'] 
            save_name = "{}.jpg".format(file_id)
            if m_youporn.down_img(downfile,save_name): 
                print("down img {} {}".format(file_id,downfile))
                item['img'] = m_youporn.img_url + save_name
                item['description'] = item['description'].replace(downfile,item['img'])
                time.sleep(2.5)
            file_id += 1
            #break
    logging.debug("new rss:{}".format(rss))
    jsonstr = json.dumps(rss,ensure_ascii=False,indent=4)
    f = io.open('youporn_rss.json', 'w', encoding='utf-8')
    f.writelines(jsonstr)
    f.close()

    xml = m_youporn.json2xml('youporn_rss.json')
    with open('Rss.xml', 'w') as f:
        f.write(xml)  

if __name__ == '__main__':
    main()