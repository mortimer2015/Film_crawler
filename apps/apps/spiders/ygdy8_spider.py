# -*- coding: utf-8 -*-
import requests
from re import split, compile

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from apps import settings

name_compile = compile(r'\[[0-9]{2}\.[0-9]{2}\].*')
name1_compile = compile(r'^\s*\[.*\]\s*$')
s = 'https://oapi.dingtalk.com/robot/send?access_token={}'.format(settings.DINGTALK_TOKEN)


def send_text(text):
    message_content = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    requests.post(s, json=message_content)


class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['www.ygdy8.com']
    start_urls = [
        'http://www.ygdy8.com/html/gndy/dyzz/index.html',
        'http://www.ygdy8.com/html/gndy/jddy/index.html'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td/b/a'), callback='parse_item'),
    )

    def parse_item(self, response):
        movie_info = split('(<br>|<p>)', response.xpath('//p').extract()[4])
        info = ''
        with open('www.ygdy8.com', 'r+') as f:
            already_download_movie_name = set(f.readlines())
            for i in movie_info:
                if name_compile.search(i) or name1_compile.search(i):
                    if '{}\n'.format(i) in already_download_movie_name:
                        break
                    else:
                        f.write('{}\n'.format(i))
                if not i.startswith('<') and i:
                    info = '{}\n{}'.format(info, i)
            else:
                url = response.xpath('//tbody/tr/td/a/@href').extract()[0]
                info = '{}\n\n下载链接：{}\n\n详细信息页：{}'.format(
                    info,
                    url,
                    response.url
                )
                print(info)
                send_text(info)
            return None


