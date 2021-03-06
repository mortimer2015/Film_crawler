# -*- coding: utf-8 -*-
from re import split, compile

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from apps import settings
from helpers.dingtalk import send_text
from helpers.tools import spider_get_data_path, get_movie_info

name_with_time_compile = compile(r'\[[0-9]{2}\.[0-9]{2}\].*')
name_compile = compile(r'^\s*\[.*\]\s*$')
url_xpath = '//tbody/tr/td/a/@href'
movie_detail_view_xpath = '//td/b/a'
site_domains = 'www.ygdy8.com'
info_features = ('◎简', '◎片')


class Ygdy8_Spider(CrawlSpider):
    name = 'ygdy8_spider'
    allowed_domains = [site_domains]
    start_urls = [
        'http://www.ygdy8.com/html/gndy/dyzz/index.html',
        'http://www.ygdy8.com/html/gndy/jddy/index.html'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=movie_detail_view_xpath), callback='parse_item'),
    )

    def parse_item(self, response):
        movie_info = split('(<br>|<p>)', get_movie_info(response.xpath('//p').extract(), info_features))
        info = ''
        with open(spider_get_data_path(site_domains), 'r+') as f:
            already_download = set(f.readlines())
            for line in movie_info:
                if name_with_time_compile.search(line) or name_compile.search(line):
                    if '{}\n'.format(line) in already_download:
                        break
                    else:
                        f.write('{}\n'.format(line))
                if not line.startswith('<') and line:
                    info = '{}\n{}'.format(info, line)
            else:
                url = response.xpath(url_xpath).extract()[0]
                info = '{}\n\n下载链接：{}\n\n详细信息页：{}'.format(
                    info, url, response.url)
                # print info
                print(info)
                send_text(info, to=settings.DINGTALK_TOKEN)
            return None
