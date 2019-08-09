#!coding = utf-8
import time, uuid, urllib
from lxml import etree
import xmltodict
import json
import requests
import codecs


youporn_head = 'https://www.youporn.com'
categories = {
        'anal':
            {'url':'https://www.youporn.com/category/2/anal/views'},
        'japanese':
            {'url':'https://www.youporn.com/category/71/japanese/views'},
        'DP':
            {'url':'https://www.youporn.com/category/16/dp/views/'},
        'mature':
            {'url':'https://www.youporn.com/category/28/mature/'},
        'lesbian':
            {'url':'https://www.youporn.com/category/26/lesbian/'},
        'big-tits':
            {'url':'https://www.youporn.com/category/7/big-tits/'},
        'big-butt':
            {'url':'https://www.youporn.com/category/6/big-butt/'},
        'asian':
            {'url':'https://www.youporn.com/category/3/asian/'},
        'threesome':
            {'url':'https://www.youporn.com/category/38/threesome/'},
        'amateur':
            {'url':'https://www.youporn.com/category/1/amateur/'},
      }

def down_youporn_categorie_xml(categorie ,url, rss_name):
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'
    }
    response = requests.get(url=url, headers=__headers)
    html_text = str(response.content, encoding='utf-8')
    dom = etree.HTML(html_text)
    # 获取 a标签下的文本  //body/div/div[3]/div/div[4]/div[2]/div/div/a/span/img
    Hrefs = dom.xpath('//body/div/div[3]/div/div[4]/div[2]/div/div/a')
    '''     
    <item>
    <guid>Thu, 11 Jul 2019 19:00:52 GMT</guid>
    <title>Using My Big Vibrator As a Dildo</title>
    <description>&amp;lt;a href="https://www.youporn.com/watch/15251363/using-my-big-vibrator-as-a-dildo/" /&amp;gt;&amp;lt;/a&amp;gt; &amp;lt;img border="1" src="http://192.168.127.254:8080/infytb/img/2.jpg" /&amp;gt; &amp;lt;/a&amp;gt; &amp;lt;br/&amp;gt; Length: 20:55 &amp;lt;br/&amp;gt; Keywords: amateur anal big butt big tits solo girl milf webcam dildos/toys european masturbation hd</description>
    <pubDate>Thu, 11 Jul 2019 19:00:52 GMT</pubDate>
    <img>http://192.168.127.254:8080/infytb/img/2.jpg</img>
    <link>https://www.youporn.com/watch/15251363/using-my-big-vibrator-as-a-dildo/</link>
    </item>
    '''
    rss = {
        'rss': {'channel':
            {
                'item': []
            }
        }
    }

    # try:
    for item in Hrefs:
        item_data = {'title': "",
                     'link': "",
                     'description':
                         '''&lt;br/&gt;
                     &lt;img border="1" src="{}" /&gt;
                     Length:{}&lt;br/&gt;
                     Keywords:{}''',
                     'guid': "",
                     'pubDate': "Sun, 14 Jul 2019 11:00:56 GMT"
                     }
        link = str(item.xpath('./@href')[0])
        item_data['title'] = str(item.xpath('div[@class="video-box-title"]/text()')[0]).strip()
        img_url = str(item.xpath('span/img/@data-thumbnail')[0])

        if 'http' not in link:
            item_data['link'] = youporn_head+link
        else:
            item_data['link'] = link
        item_data['guid'] = item_data['link']
        print("title:{} \n img:{} \n link:{}\n  ".format(item_data['title'], img_url, item_data['link']))

        duration = str(
            item.xpath('../*/div[@class="video-duration"]/text()')[0]).strip()  # <div class="video-duration">12:35</div>
        item_data['description'] = item_data['description'].format(img_url, duration, item_data['title'])
        rss['rss']['channel']['item'].append(item_data)
    print(rss)
    xml = ''
    try:
        xml = xmltodict.unparse(rss, encoding='utf-8')
        print(xml)
    # except:
    #    xml = xmltodict.unparse({'request': channel}, encoding='utf-8')
    #    print(xml)
    finally:
        with codecs.open(rss_name, 'w', 'utf-8') as f:
            f.write(xml)
    return True

categorie_rss={'rss':
                   {'categorie':
                        {'item':[]}
                    }
               }
for categorie,data in categories.items():
    rss_name = 'youporn_{}_rss.xml'.format(categorie)
    state = down_youporn_categorie_xml(categorie, data['url'], rss_name)
    data['state'] = state
    data['rss'] = rss_name
    if(state == True) :
        categorie_data = {'title':None,'link':None}
        categorie_data['title'] = categorie
        categorie_data['link'] = "{}/{}".format(youporn_head,rss_name)
        categorie_rss['rss']['categorie']['item'].append(categorie_data)
    time.sleep(2.5)

print(categorie_rss)
xml = ''
try:
    xml = xmltodict.unparse(categorie_rss, encoding='utf-8')
    print(xml)
# except:
#    xml = xmltodict.unparse({'request': channel}, encoding='utf-8')
#    print(xml)
finally:
    with codecs.open('youporn_categorie_rss.xml', 'w', 'utf-8') as f:
        f.write(xml)