# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class ZhaopinSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://passport.zhaopin.com/org/login']

    headers = {
        'Host': 'passport.zhaopin.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'
    }

    def start_requests(self):
        return [Request("https://passport.zhaopin.com/org/login",
                        meta={'dont_redirect': True,
                              'handle_httpstatus_list': [301, 302],
                              'cookiejar': 1},
                        callback=self.parse_login_html)]

    def parse_login_html(self, response):
        print response.body
        print response.headers

        yield Request("https://passport.zhaopin.com/org/login", meta={"cookiejar": True}, callback=self.parse_login)
        
    def parse_login(self, response):
        print response.body
