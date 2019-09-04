# -*- coding: utf-8 -*-
import scrapy
import lxml
import xmltodict
from lxml import etree
from xml.dom.minidom import Document
from youporn.items import YoupornItem

YOUPORN_HEAD = 'https://www.youporn.com'
YOUPORN_ALL_CATEGORES = 'https://www.youporn.com/categories/'


class YoupornitemSpider(scrapy.Spider):
    name = 'youpornitem'
    allowed_domains = ['youporn.com']
    start_urls = ['https://www.youporn.com/categories/']

    def parse(self, response):
        #print(response.text)
        category_list = self.analysis_all_categores(response)
        #print(category_list)

        for class_item in category_list:
            for son_item in class_item['son']:
                rss_name = 'youporn_{}_rss.xml'.format(son_item['title'])
                next_link = "{}{}".format(YOUPORN_HEAD, son_item['link'])
                #print('next_link:',next_link)
                if next_link is not None:
                    yield scrapy.Request(next_link, meta={'name': rss_name,'class1':class_item['class_parents'],'class2':class_item['class_name'] ,'class3':son_item['title']}, callback=self.anlysis_youporn_item)



    # 分析具体单个类别数据
    def anlysis_youporn_item(self,response):
        # 获取 a标签下的文本  //body/div/div[3]/div/div[4]/div[2]/div/div/a/span/img
        Hrefs = response.xpath('//body/div/div[3]/div/div[4]/div[2]/div/div/a')
        class1 = response.meta['class1']
        class2 = response.meta['class2']
        class3 = response.meta['class3']

        #print('class1,class2,class3:',class1,class2,class3)
        Youpornitems = []

        for item in Hrefs:
            item_data = {'title': "",
                        'link': "",
                        'description': '&lt;br/&gt; &lt;img border="1" src="{}" /&gt;Length: {}&lt;br/&gt;Keywords:{}',
                        'guid': "",
                        'pubDate': "Sun, 14 Jul 2019 11:00:56 GMT"
                        }
            link = str(item.xpath('./@href').extract()[0])
            item_data['title'] = str(item.xpath('div[@class="video-box-title"]/text()').extract()[0]).strip()
            img_url = str(item.xpath('span/img/@data-thumbnail').extract()[0])

            if 'http' not in link:
                item_data['link'] = YOUPORN_HEAD + link
            else:
                item_data['link'] = link
            item_data['guid'] = item_data['link']
            duration = str(item.xpath('../*/div[@class="video-duration"]/text()').extract()[0]).strip()
            item_data['description'] = item_data['description'].format(img_url, duration, item_data['title'])
    
            Youpornitem = YoupornItem()
            Youpornitem['class1']   = class1
            Youpornitem['class2']   = class2
            Youpornitem['class3']   = class3
            Youpornitem['title']    = item_data['title']
            Youpornitem['link']     = item_data['link']
            Youpornitem['description'] = item_data['description']
            Youpornitem['guid']        = item_data['guid']
            Youpornitem['pubDate']     = item_data['pubDate']
            Youpornitems.append(Youpornitem)
        #print(Youpornitems)
        return Youpornitems


#分析所有类型URL
    def analysis_all_categores(self,dom):
        class1 = dom.xpath('//div[contains(@class,"categories_list") and contains(@class,"porn-categories")]')
        classlist = []
        for class1_item in class1:
            class_dict = {'class_parents':None,'class_name':None,'son':[]}
            class0_name = str(class1_item.xpath('preceding-sibling::div[@class="title-bar"]/div/div/h2/text()').extract()[-1]).strip()
            class1_name = str(class1_item.xpath('span[@class ="category-list-title"]/text()').extract()[0]).strip()
            #print('class0:class1',class0_name,class1_name)
            
            category_title_div = class1_item.xpath('div/a/div[@class="categoryTitle"]')
            for item in category_title_div:
                href = str(item.xpath('../@href').extract()[0]).strip()
                # title = str(item.xpath('p/text()')[0]).strip()
                # '/category/44/dildos-toys/' 直接从url中取类型 避免path出现非法字符
                title = href.split('/')[-2]
                category_dict = {}
                category_dict['title'] = title.strip().title()
                category_dict['link'] = href
                class_dict['son'].append(category_dict)
            class_dict['class_parents'] = class0_name.title()
            class_dict['class_name'] = class1_name.title()
            classlist.append(class_dict)
        return classlist
