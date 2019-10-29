# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import json
import time
import scrapy
from six.moves.urllib.parse import urljoin
from w3lib.url import safe_url_string
import uuid


class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
        # 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
        # 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent

class IPProxyDownloadMiddleware(object):
    PROXIES = [
        "http://167.71.142.245:8080",
        "http://62.210.124.248:3128",
        "http://163.172.136.226:8811",
        "http://47.90.83.213:8888",
        "http://222.197.182.108:3128",
        "http://140.143.48.49:1080"
    ]

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = proxy

class cookiesDownloadMiddleware(object):
    # 获取计数器number,并保存至文本
    def get_number(self):
        while True:
            try:
                with open("number.txt", "r") as f:
                    number = f.read()
                    break
            except:
                # 创造计数器
                with open("number.txt", "w") as f:
                    number = 0
                    f.write(str(number))
            # if not number:
            #     number = 0
        number = int(str(number))
        number += 1
        with open("number.txt", "w") as f:
            f.write(str(number))
        self.number = number

    # 将传入的字符串数字+number
    def str_plus(self, strnum):
        num = int(strnum)
        num += self.number
        return str(num)

    # 获取cookie
    def get_cookie(self):
        with open("zpcookies.json", "r") as f:
            listcookies = json.load(f)
        # 对获取的cookie进行修改
        for i in listcookies:
            if i["name"] == "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a":
                i["value"] = str(int(time.time()))
            elif i["name"] == "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a":
                i["value"] = str(int(time.time()))
                self.c = i["value"]
            elif i["name"] == "_bl_uid":
                uid = str(uuid.uuid4())
                i["value"] = ''.join(uid.split('-')[1:])
            elif i["name"] == "__a":
                a_list = []
                for a in i["value"]:
                    a_list.append(a)
                a_list[-1] = self.str_plus(a_list[-1])
                a_list[-3] = self.str_plus(a_list[-3])
                a_list[-7] = self.str_plus(a_list[-7])
                a_list = "".join(a_list)
                i["value"] = a_list
                print(a_list)
        for i in listcookies:
            if i["name"] == "__c":
                i["value"] = self.c
        return listcookies
    def process_request(self, request, spider):
        # cookie = random.choice(self.COOKIES)
        self.get_number()
        request.cookies = self.get_cookie()


class RedirectMiddleware(object):
    pass