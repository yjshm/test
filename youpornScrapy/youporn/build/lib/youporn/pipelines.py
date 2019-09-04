# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import lxml
import xmltodict
import copy
from xml.dom.minidom import Document

from operator import itemgetter  # itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby  # itertool还包含有其他很多函数，比如将多个list联合起来。。
import json

RELAY_SEVER_HEAD = 'http://192.168.127.254:8080/infytb'

class YoupornPipeline(object):
    items = None

    def __init__(self):
        ##self.fo = open('youpornsave.txt', 'wb')
        self.items = []

    def process_item(self, item, spider):
        # sorted(item.items(), key=lambda i:i["class1"])
        '''
        self.fo.write((item['class1'] + '\n').encode('utf-8'))
        self.fo.write((item['class2'] + '\n').encode('utf-8'))
        self.fo.write((item['class3'] + '\n').encode('utf-8'))
        self.fo.write((item['title'] + '\n').encode('utf-8'))
        self.fo.write((item['link'] + '\n').encode('utf-8'))
        self.fo.write((item['description'] + '\n').encode('utf-8'))
        self.fo.write((item['guid'] + '\n').encode('utf-8'))
        self.fo.write((item['pubDate'] + '\n').encode('utf-8'))
        self.fo.flush()
        '''
        # 这里必须返回item，否则程序会一直等待，直到返回item为止
        item2 = {}
        item2['class1'] = item['class1']
        item2['class2'] = item['class2']
        item2['class3'] = item['class3']
        item2['title'] = item['title']
        item2['link'] = item['link']
        item2['description'] = item['description']
        item2['guid'] = item['guid']
        item2['pubDate'] = item['pubDate']
        self.items.append(item2)

        return item

    def close_spider(self, spider):
        # 保存所有单个分类点播RSS
        self.items.sort(key=itemgetter('class1','class2','class3'))  # 需要先排序，然后才能groupby。lst排序后自身被改变
        items_group = groupby(self.items, itemgetter('class1', 'class2','class3'))
        for key, group in items_group:
            rss = {
                'rss': {'channel':
                    {
                        'item': []
                    }
                }
            }
            for item in group:  # group是一个迭代器，包含了所有的分组列表
                # print key,item
                item2 = {}
                item2['title'] = item['title']
                item2['link'] = item['link']
                item2['description'] = item['description']
                item2['guid'] = item['guid']
                item2['pubDate'] = item['pubDate']
                rss['rss']['channel']['item'].append(item2)
                # print(result)
            self.save_as_xml_rss(rss, './rss/youporn_{}_rss.xml'.format(item['class3']))

        # 保存类型RSS
        self.items.sort(key=itemgetter('class1','class2','class3'))  # 需要先排序，然后才能groupby。lst排序后自身被改变
        struct_data = self.convert_struct(self.items)
        self.save_class_as_xml(struct_data, './rss/youporn_categorie_rss.xml')
        #self.fo.close()

    # 保存单个类型rss文件
    def save_as_xml_rss(self, rss, file_name):
        xml = ''
        try:
            xml = xmltodict.unparse(rss, encoding='utf-8')
        finally:
            with codecs.open(file_name, 'w', 'utf-8') as f:
                f.write(xml)
        return True


    # items数数转化成结构化分类数据
    # 返回 : {'Action': {'ACTION':{'Teen':'http://www.xxx.com/xxrss.xml'} }
    def convert_struct(self, rss):
        class1s = {}
        for item in rss:
            xml_class1 = item['class1']
            xml_class2 = item['class2']
            xml_class3 = item['class3']
            if xml_class1 not in class1s:
                class1s[xml_class1] = {}
            if xml_class2 not in class1s[xml_class1]:
                class1s[xml_class1][xml_class2] = {}
            if xml_class3 not in class1s[xml_class1][xml_class2]:
                class1s[xml_class1][xml_class2][xml_class3] = {}
            class1s[xml_class1][xml_class2][xml_class3] = '{}/youporn_{}_rss.xml'.format(RELAY_SEVER_HEAD, item['class3'])
        return class1s

    # 保存全部分类文件
    def save_class_as_xml(self, rss, file_name):
        doc = Document()
        rss_xml = doc.createElement('rss')
        categorie = doc.createElement('categorie')
        for class1_name,class1_item in rss.items() :
            class1 = doc.createElement('class1')
            class1_title = doc.createElement('title')
            objectcontenttext = doc.createTextNode(class1_name)
            class1_title.appendChild(objectcontenttext)
            class1.appendChild(class1_title)
            for class2_name, class2_item in class1_item.items():
                class2 = doc.createElement('class2')
                class2_title = doc.createElement('title')
                objectcontenttext = doc.createTextNode(class2_name)
                class2_title.appendChild(objectcontenttext)
                class2.appendChild(class2_title)
                for class3_name, class3_item in class2_item.items():
                    item = doc.createElement('item')
                    item_title = doc.createElement('title')
                    objectcontenttext = doc.createTextNode(class3_name)
                    item_title.appendChild(objectcontenttext)
                    item.appendChild(item_title)

                    item_link = doc.createElement('link')
                    objectcontenttext = doc.createTextNode(class3_item)
                    item_link.appendChild(objectcontenttext)
                    item.appendChild(item_link)
                    class2.appendChild(item)
                class1.appendChild(class2)
            categorie.appendChild(class1)
        rss_xml.appendChild(categorie)
        doc.appendChild(rss_xml)

        with  open(file_name, 'w') as fp:
            doc.writexml(fp, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
