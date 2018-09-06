# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class BeautylegPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['pic_name']
        image_name = request.url.split('/')[-1]
        image_name = image_name.split("-")[-1]
        filename = u'Picture/{0}/{1}'.format(folder, image_name)
        return filename

    def get_media_requests(self, item, info):
        for img_url in item['pic_urls']:
            yield Request(img_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
