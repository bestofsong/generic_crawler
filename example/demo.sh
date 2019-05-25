#!/usr/bin/env bash
scrapy crawl generic -a url='https://www.xiaopian.com/html/gndy/dyzz/index.html' -a conf=example/xiaopian.yml -o xiaopian.jl
