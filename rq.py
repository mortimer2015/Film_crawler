# -*- coding: utf8 -*-
import requests
import re
import traceback


zz = re.compile(r'href="magnet:.*"')
url_c = re.compile(r'href="(.*)"')
title_c = re.compile(r'title="(.*)"')
name_c = re.compile(r'class="ulink">(.*)</a>')
get_movie_link_c = re.compile(r'href="(.*)">ftp://.*')
m_movie_c = re.compile(r"^\r\n<a href='(.*)'>(.*)</a>")
movie_information_c = re.compile(u"^(◎.*)")
s = 'https://oapi.dingtalk.com/robot/send?access_token=' \
    'YOUR TOKEN'


def send_text(text):
    message_content = {
        "msgtype": "text",
        "text": {
            "content": text,
        }
    }
    requests.post(s, json=message_content)


def get_new_soap_opera(soap_opera=None):
    try:
        data = requests.get(soap_opera['url'])
        data.encoding = 'gb2312'
        data = data.text.split()
        for k, v in enumerate(data):
            if zz.search(v):
                url = url_c.search(v).groups()[0]
                title = title_c.search(data[k + 1]).groups()[0]
                with open('magnet.txt', 'r+') as f:
                    old_magnet = f.readlines()

                    if '{}\n'.format(url) not in old_magnet:
                        send_text('<{}>{}，下载链接：{}'.format(
                            soap_opera['name'],
                            title.encode('utf8'), url))
                        f.write('{}\n'.format(url))
    except:
        send_text('大佬，{}挂了！'.format(soap_opera['url']))


def get_movie_link_information(url):
    data = requests.get(url)
    data.encoding = 'gb2312'
    d = data.text.split('<br />')
    mv_if = []
    for i in d:
        information = movie_information_c.search(i)
        if information:
            d = information.groups()[0]
            if d.startswith('◎上映日期'.decode('utf8')) or d.startswith('◎简'.decode('utf8')):
                continue
            mv_if.append(d)
    mv_if_str = '\n'.join(mv_if)

    for i in data.text.split():
        link = get_movie_link_c.search(i)
        if link:
            return link.groups()[0], mv_if_str


def get_new_movie(page):
    try:
        data = requests.get(page)
        data.encoding = 'gb2312'
        data = data.text.split()
        for k, v in enumerate(data):
            d = name_c.search(v)
            if d:
                url = '{}{}'.format('http://www.ygdy8.com', data[k - 1].split('"')[1])
                name = d.groups()[0]
                with open('movie.txt', 'r+') as f:
                    old_movie = f.readlines()
                    if '{}\n'.format(name.encode('utf8')) not in old_movie:
                        link, information = get_movie_link_information(url)
                        movie_data = '{}\n\n{}\n\n下载链接：{}\n\n电影详细信息：{}'.format(
                            name.encode('utf8'),
                            information.encode('utf8'),
                            link.encode('utf8'),
                            url.encode('utf8'))
                        send_text(movie_data)
                        print(movie_data)
                        f.write('{}\n'.format(name.encode('utf8')))
                    # else:
                    #     print('已经下载了')
    except Exception as e:
        print(traceback.format_exc(e))
        print('大佬，{}网站挂了！'.format('http://www.ygdy8.com/'))


# def get_movie(page):
#     try:
    # data = requests.get(page)
    # data.encoding = 'gb2312'
    # data = data.text.split('<br/>')
    # for k, v in enumerate(data):
    #     d = m_movie_c.search(v)
    #     if d:
    #         url = '{}{}'.format('http://www.ygdy8.com', d.groups()[0])
    #         name = d.groups()[1]
    #         with open('movie.txt', 'r+') as f:
    #             old_movie = f.readlines()
    #             if '{}\n'.format(name.encode('utf8')) not in old_movie:
    #                 link = get_movie_link(url)
    #                 print('{}，下载链接：{}'.format(name.encode('utf8'), link.encode('utf8')))
    #                 f.write('{}\n'.format(name.encode('utf8')))
    #             else:
                #     print('已经下载了')
    # except Exception, e:
    #     print('大佬，{}网站挂了！'.format('http://www.ygdy8.com/'))


if __name__ == '__main__':
    soap_operas = [
        {'name': '西部世界', 'url': 'https://www.loldytt.com/Zuixinmeiju/XBSJDEJ/'}
    ]
    for soap_opera in soap_operas:
        get_new_soap_opera(soap_opera)
    movie_page_list = ['http://www.ygdy8.com/html/gndy/jddy/index.html',
                       'http://www.ygdy8.com/html/gndy/dyzz/index.html']
    for movie_page in movie_page_list:
        get_new_movie(movie_page)
    # movie_page = ['http://www.ygdy8.com']
    # for i in movie_page:
    #     get_movie(i)
