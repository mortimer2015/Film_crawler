#!/bin/bash
cd apps
scrapy crawl movie_list
scrapy crawl send_movie_info
