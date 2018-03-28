# -*- coding: utf-8 -*-
"""
智联登录
Author: Marico
Version: 1.0.1
Date: 2017-11-15
Language: Python 2.7.13
"""
from scrapy import cmdline

name = 'zhilian'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())