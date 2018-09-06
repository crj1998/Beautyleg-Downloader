#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/30 16:53
#!Author: Renjie Chen
#!Function:

from scrapy.cmdline import execute
execute(['scrapy','crawl','Beautyleg','-a','indexlist=1629'])