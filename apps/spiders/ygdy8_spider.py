# -*- coding: utf-8 -*-
from re import split, compile

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from apps import settings
from helpers.dingtalk import send_text
from helpers.tools import spider_get_data_path

name_start_time_compile = compile(r'\[[0-9]{2}\.[0-9]{2}\].*')
name_compile = compile(r'^\s*\[.*\]\s*$')
url_xpath = '//tbody/tr/td/a/@href'
movie_detail_view_xpath = '//td/b/a'
site_domains = 'www.ygdy8.com'


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
        # hardcode
        movie_info = split('(<br>|<p>)', response.xpath('//p').extract()[4])
        info = ''
        with open(spider_get_data_path(site_domains), 'r+') as f:
            already_download_movie_name = set(f.readlines())
            for line in movie_info:
                if name_start_time_compile.search(line) or name_compile.search(line):
                    if '{}\n'.format(line) in already_download_movie_name:
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
