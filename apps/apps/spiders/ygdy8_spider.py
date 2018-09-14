# -*- coding: utf-8 -*-
import scrapy
import requests
from re import split

from apps import settings


class DmozSpider(scrapy.Spider):

    name = "movie_list"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        'http://www.ygdy8.com/html/gndy/dyzz/index.html',
        'http://www.ygdy8.com/html/gndy/jddy/index.html'
    ]

    def parse(self, response):
        base_name = 'http://www.ygdy8.com'
        filename = response.url.split("/")[2]
        with open(filename, 'r+') as f:
            file_list = f.read().split('\n')
            with open('tmp.txt', 'r+') as tmp:
                for i in response.xpath('//td/b'):
                    url = i.xpath('a/@href').extract()[0]
                    name = i.xpath('a/text()').extract()[0]
                    print(url, name)
                    if name not in file_list:
                        f.write('{}\n'.format(name))
                        tmp.write('{}{}\n'.format(base_name, url))


token = settings.DINGTALK_TOKEN
s = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(token)


def send_text(text):
    message_content = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    requests.post(s, json=message_content)


class DetailSpider(scrapy.Spider):
    name = "send_movie_info"
    allowed_domains = ["dmoz.org"]
    with open('tmp.txt', 'r+') as f:
        start_urls = f.read().split()
    with open('tmp.txt', 'w') as f:
        pass

    def parse(self, response):
        movie_info = split('(<br>|<p>)', response.xpath('//p').extract()[4])
        info = ''
        for i in movie_info:
            if not i.startswith('<') and i:
                info = '{}\n{}'.format(info, i)
        url = response.xpath('//tbody/tr/td/a/@href').extract()[0]
        info = '{}\n\n下载链接：{}\n\n详细信息页：{}'.format(
            info,
            url,
            response.url
        )
        print(info)
        send_text(info)
