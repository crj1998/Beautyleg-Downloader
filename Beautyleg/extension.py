from scrapy import signals
class Beautylegextensions(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.item_scraped, signal=signals.item_scraped)
        return s

    def item_scraped(self,item, response, spider):
        print("now @: ",item["pic_name"])

