#!/usr/bin/env bash
scrapy crawl generic -a url='https://list.jd.com/list.html?cat=670,671,672' -a conf=example/jd.json -o jd.jl
