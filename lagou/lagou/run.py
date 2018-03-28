# -*- coding: utf-8 -*-
"""
拉勾网登录
Author: Marico
Version: 1.0.1
Date: 2017-11-14
Language: Python 2.7.13
"""

from scrapy import cmdline

name = 'lagou'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())