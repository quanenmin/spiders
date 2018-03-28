# -*- coding: utf-8 -*-
"""
拉勾网登录
Author: Marico
Version: 1.0.1
Date: 2017-11-14
Language: Python 2.7.13
"""
import re

from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider
from lagou.utils.Md5 import encrypt
import urllib

class LagouSpider(CrawlSpider):
    name = "lagou"
    allowed_domains = ["passport.lagou.com"]

    start_urls = [
        "https://easy.lagou.com/can/index.htm?can=true&stage=NEW&needQueryAmount=true&parentPositionIds="
    ]

    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
        "Host": "easy.lagou.com"
    }

    # 重写爬虫类方法，实现自定义请求，运行成功后会回调callback函数
    def start_requests(self):
        return [Request("https://easy.lagou.com/can/index.htm?can=true&stage=NEW&needQueryAmount=true&parentPositionIds=",
                        meta={'dont_redirect': True,
                              'handle_httpstatus_list': [301, 302],
                              'cookiejar': 1},
                        callback=self.parse_login_html)]

    # 重定向到登录页面
    def parse_login_html(self, response):
        yield Request(response.headers["Location"], meta={"cookiejar": True}, callback=self.login_html)

    # 登录页面
    def login_html(self, response):
        (x_code, x_token) = self.findCodeAndToken(response.body)

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'passport.lagou.com',
            'Origin': 'https://passport.lagou.com',
            'Pragma': 'no-cache',
            # 'Referer': referer,
            'X-Requested-With': 'XMLHttpRequest',
            'X-Anit-Forge-Token': x_token,
            'X-Anit-Forge-Code': x_code
        }

        # 模拟登录数据
        name = "*******"
        pwd = "******"
        pwd = encrypt('veenike' + encrypt(pwd) + 'veenike')

        data = {
            'isValidate': 'true',
            'username': name,
            'password': pwd,
            'request_form_verifyCode': '',
            'submit': ''
        }

        headers['Content-Length'] = str(len(urllib.urlencode(data)))

        yield FormRequest("https://passport.lagou.com/login/login.json", meta={"cookiejar": True}, formdata=data, callback=self.login_result)

    def login_result(self, response):
        print response.body

    # 获取anit_code|anit_token
    def findCodeAndToken(self, content):
        '''
        解析Html，读取x_anit_forge_code、x_anit_forge_token
        '''
        soap = BeautifulSoup(content)
        if soap is None:
            print('Response Body is None')
            return False

        x_forge = soap.find(text=re.compile("window.X_Anti_Forge_Token"))

        if x_forge is None:
            print('X_Anit_Forge_* is None')
            return False

        strs = x_forge.split('\n')
        for _str in strs:
            if 'X_Anti_Forge_Code' in _str:
                x_forge_code = _str.split('=')[1].strip(' ').replace('\'', '').replace(';', '')
            if 'X_Anti_Forge_Token' in _str:
                x_forge_token = _str.split('=')[1].strip(' ').replace('\'', '').replace(';', '')

        return x_forge_code, x_forge_token
