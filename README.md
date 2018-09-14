# 电影爬虫

这个爬虫主要是爬`http://www.ygdy8.com/`网站，爬取的数据有电影的信息、下载链接、下载网页。

## 依赖

python3，下载安装请参考`https://www.python.org/`

依赖包使用pipenv安装，pipenv的安装方法请参考`https://github.com/pypa/pipenv`

```bash
git clone https://github.com/mortimer2015/Film_crawler.git
cd Film_crawler
pipenv install
pipenv shell
```

## 使用方法

配置文件`cp apps/apps/secrets_example.py apps/apps/secrets.py`


运行当前目录下的的`run.sh`文件

```bash
run.sh
```
