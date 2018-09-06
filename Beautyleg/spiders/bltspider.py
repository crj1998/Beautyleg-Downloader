#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/25 19:08
#!Author: Renjie Chen
#!Function:

import scrapy
from Beautyleg.items import BeautylegItem
import csv


class bltSpider(scrapy.Spider):
    name = "Beautyleg"
    def __init__(self,indexlist=None):
        self.index_list = [int(no)-1 for no in indexlist.split(",")]
        self.start_urls = ["http://www.beautylegmm.com/"]
        self.allowed_domains = ["beautylegmm.com"]

    def parse(self, response):
        with open("res/1.data", "r", encoding="utf-8") as csvFile:
            lines = [l for l in csv.reader(csvFile, delimiter='-')]
            line = [lines[no] for no in self.index_list]
        for index in line:
            item = BeautylegItem()
            item["pic_name"] = 'No.%s %s'%(index[1],index[2])
            pic_urls = []
            for page in range(int(index[3])):
                pic_url = 'http://www.beautylegmm.com/photo/beautyleg/%s/%s/beautyleg-%s-%s.jpg' % (
                index[0], index[1], index[1], str(page).zfill(4))
                pic_urls.append(pic_url)
            item["pic_urls"] = pic_urls
            yield item