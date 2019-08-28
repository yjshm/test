#!endcoding = utf-8  python3.7
import codecs
import time
from urllib import request

import lxml
import xmltodict
from lxml import etree
from xml.dom.minidom import Document

YOUPORN_HEAD = 'https://www.youporn.com'
RELAY_SEVER_HEAD = 'http://192.168.127.254:8080/infytb'
YOUPORN_ALL_CATEGORES = 'https://www.youporn.com/categories/'


def download_html(url, mytype):
    Html = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    print('download_html:' + url)
    try:
        req = request.Request(url=url, headers=headers)
        data = request.urlopen(req).read();
        if data:
            Html = str(data, encoding='utf-8')
    finally:
        return Html

'''
def save_as_xml(rss, file_name):
    xml = ''
    try:
        xml = xmltodict.unparse(rss, encoding='utf-8')
        print(xml)
    # except:
    #    xml = xmltodict.unparse({'request': channel}, encoding='utf-8')
    #    print(xml)
    finally:
        with codecs.open(file_name, 'w', 'utf-8') as f:
            f.write(xml)
    return True
'''


''' xml式样
<?xml version="1.0" encoding="utf-8"?>
<rss>
    <categorie>
        <class1>
            <title>recommand</title>
            <class2>
                <title>recommand</title>
                <item>
                    <title>lesbian</title>
                    <link>http://192.168.127.254:8080/infytb/youporn_lesbian_rss.xml</link>
                </item>
                <item>
                    <title>college</title>
                    <link>http://192.168.127.254:8080/infytb/youporn_college_rss.xml</link>
                </item>
			</class2>
		</class1>
	</categorie>
</rss>'''
def save_as_xml(rss, file_name):
    doc = Document()

    rss_xml = doc.createElement('rss')
    categorie = doc.createElement('categorie')
    for class1_item in rss:
        class1 = doc.createElement('class1')
        class1_title = doc.createElement('title')
        objectcontenttext = doc.createTextNode(class1_item['class1']['title'])
        class1_title.appendChild(objectcontenttext)
        class1.appendChild(class1_title)
        for class2_item in class1_item['class1']['data']:
            class2 = doc.createElement('class2')
            class2_title = doc.createElement('title')
            objectcontenttext = doc.createTextNode(class2_item['class2']['title'])
            class2_title.appendChild(objectcontenttext)
            class2.appendChild(class2_title)
            item_data =class2_item['class2']['data']
            for item_item in item_data['item']['data']:
                item = doc.createElement('item')
                item_title = doc.createElement('title')
                objectcontenttext = doc.createTextNode(item_item['title'])
                item_title.appendChild(objectcontenttext)
                item.appendChild(item_title)

                item_link = doc.createElement('link')
                objectcontenttext = doc.createTextNode(item_item['link'])
                item_link.appendChild(objectcontenttext)

                item.appendChild(item_link)
                class2.appendChild(item)
            class1.appendChild(class2)
        categorie.appendChild(class1)
    rss_xml.appendChild(categorie)
    doc.appendChild(rss_xml)

    with  open(file_name, 'w') as fp:
        doc.writexml(fp, indent='\t', newl='\n', addindent='\t', encoding='utf-8')


def analysis_all_categores(url):
    Html = download_html(url, 1)
    #with open('PornCategories.html','r') as fp:
    #    Html = fp.read()

    if (not Html):
        return None
    mytree = lxml.etree.HTML(Html)
    # class ="categories_list porn-categories sixteen-column action" >  <span class="category-list-title">
    class1 = mytree.xpath('//div[contains(@class,"categories_list") and contains(@class,"porn-categories")]')

    class1_list = {}
    for class1_item in class1:
        class1_name = str(class1_item.xpath('span[@class ="category-list-title"]/text()')[0]).strip()
        print(class1_name)

        # print(mytree.xpath('//*[@id="categoryList"]/*/div[@class="categoryTitle"]/../@href'))
        # print(mytree.xpath('//*[@id="categoryList"]/*/div[@class="categoryTitle"]/p/text()'))
        category_dict = {};
        category_title_div = class1_item.xpath('div/a/div[@class="categoryTitle"]')
        for item in category_title_div:
            href = str(item.xpath('../@href')[0]).strip()
            # title = str(item.xpath('p/text()')[0]).strip()
            # '/category/44/dildos-toys/' 直接从url中取类型 避免path出现非法字符
            title = href.split('/')[-2]
            category_dict[title] = href
        print(category_dict)
        class1_list[class1_name] = category_dict
    return class1_list


# 分析具体单个类别数据
def anlysis_categorie(url):
    html_text = download_html(url, 1)
    if (not html_text):
        return None
    dom = lxml.etree.HTML(html_text)
    # 获取 a标签下的文本  //body/div/div[3]/div/div[4]/div[2]/div/div/a/span/img
    Hrefs = dom.xpath('//body/div/div[3]/div/div[4]/div[2]/div/div/a')
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
                     'description': '''&lt;br/&gt; &lt;img border="1" src="{}" /&gt;Length:{}&lt;br/&gt;Keywords:{}''',
                     'guid': "",
                     'pubDate': "Sun, 14 Jul 2019 11:00:56 GMT"
                     }
        link = str(item.xpath('./@href')[0])
        item_data['title'] = str(item.xpath('div[@class="video-box-title"]/text()')[0]).strip()
        img_url = str(item.xpath('span/img/@data-thumbnail')[0])

        if 'http' not in link:
            item_data['link'] = YOUPORN_HEAD + link
        else:
            item_data['link'] = link
        item_data['guid'] = item_data['link']
        print("title:{} \n img:{} \n link:{}\n  ".format(item_data['title'], img_url, item_data['link']))

        duration = str(
            item.xpath('../*/div[@class="video-duration"]/text()')[0]).strip()
        item_data['description'] = item_data['description'].format(img_url, duration, item_data['title'])
        rss['rss']['channel']['item'].append(item_data)
    print(rss)
    return rss
    # save_as_xml(rss)

def build_class(class_tag,class_title,data):
    class_list={class_tag:{'title':class_title,'data':data}}
    return class_list

def down_all_categories():
    categories_rss = {'rss':
        {'categorie':[
            #{'class1':['title':None, {'class1' : None}]}
            ]
        }
    }
    categories_rss['rss']['categorie'].clear()
    dict_all_categores = analysis_all_categores(YOUPORN_ALL_CATEGORES)

    class_list = [];
    class1_list = [];
    #class1_list.append({'title': 'recommand'})
    for class2, class2_item in dict_all_categores.items():
        item_list = []
        for categorie, src in class2_item.items():
            rss_name = 'youporn_{}_rss.xml'.format(categorie)
            '''rss_categorie = anlysis_categorie("{}{}".format(YOUPORN_HEAD, src))
            # data['state'] = state
            # data['rss'] = rss_name
            if (rss_categorie):e
                save_as_xml(rss_categorie, rss_name)
            '''
            categorie_data = {}
            categorie_data['title'] = categorie
            categorie_data['link'] = "{}/{}".format(RELAY_SEVER_HEAD, rss_name)
            item_list.append(categorie_data)
            print(categories_rss)
            #time.sleep(3)
        item_dict = None
        item_dict = build_class('item', 'ItemTitle', item_list)
        class2_dict = build_class('class2',class2,item_dict)
        #print(class2_dict)
        class1_list.append(class2_dict)

    class1_dict = build_class('class1','recommand', class1_list)
    class_list.append(class1_dict)
    print(class_list)
    save_as_xml(class_list, 'youporn_categorie_rss.xml')

print('xpath ')
#save_as_xml(None,'youporn_categorie_rss.xml')
down_all_categories()
