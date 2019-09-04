# -*- coding: utf-8 -*-
import os
import time
import datetime

if __name__ == '__main__':
    while True:
        print('run>>>>', datetime.datetime.now().strftime('%a, %d %b %Y %X %Z GMT'))
        os.system('scrapy crawl youpornitem')
        print('run<<< ',datetime.datetime.now().strftime('%a, %d %b %Y %X %Z GMT'))
        time.sleep(5*60)
